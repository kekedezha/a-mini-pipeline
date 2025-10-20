import json
import re
import sqlite3
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import SystemMessage, HumanMessage

# --- Load environment variables ---
load_dotenv()

# --- Initialize the LLM ---
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
)

# --- Connect to SQLite ---
DB_PATH = Path(__file__).resolve().parent.parent / "database" / "a2_pipeline.db"
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql("SELECT * FROM products", conn)

# --- Load prompt template ---
PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "product_prompt.txt"
prompt_text = open(PROMPT_PATH).read()

prompt = PromptTemplate(
    input_variables=["product_data"],
    template=prompt_text
)

results = []

for _, row in df.iterrows():
    product_data = row.to_dict()
    product_name = product_data["product_name"]

    print(f"🧠 Generating structured SEO output for: {product_name}")

    # Convert product data to JSON string for prompt
    product_json = json.dumps(product_data, indent=2)

    # Format the prompt with product data
    formatted_prompt = prompt.format(product_data=product_json)

    # Format input for the model
    messages = [
        SystemMessage(content="You are a helpful SEO assistant that always returns valid JSON."),
        HumanMessage(content=prompt.format(product_data=json.dumps(product_data, indent=2)))
    ]

    try:
        # --- Get model response ---
        response = llm.invoke(messages)
        ai_text = str(response.content).strip()  # safe cast to str for Pylance

        # --- Clean model output (remove markdown, extract JSON only) ---
        cleaned = re.sub(r"```(?:json)?", "", ai_text)
        cleaned = cleaned.replace("```", "").strip()

        # Extract JSON substring if there’s extra commentary
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            cleaned = match.group(0)

        # --- Try to parse JSON ---
        try:
            ai_json = json.loads(cleaned)
        except json.JSONDecodeError:
            print(f"⚠️ Could not parse JSON for {product_name}. Retrying with explicit JSON fix prompt...")

            fix_prompt = f"Return only valid JSON from the following text. Do not add commentary:\n\n{ai_text}"
            fix_response = llm.invoke([HumanMessage(content=fix_prompt)])
            cleaned_fixed = re.sub(r"```(?:json)?", "", str(fix_response.content))
            cleaned_fixed = cleaned_fixed.replace("```", "").strip()
            match_fixed = re.search(r"\{.*\}", cleaned_fixed, re.DOTALL)
            if match_fixed:
                cleaned_fixed = match_fixed.group(0)
            ai_json = json.loads(cleaned_fixed)

        # --- Merge parsed fields into structured row ---
        results.append({
            "product_id": product_data["product_id"],
            "product_name": product_name,
            "meta_title": ai_json.get("meta_title", ""),
            "meta_description": ai_json.get("meta_description", ""),
            "product_description": ai_json.get("product_description", "")
        })

    except Exception as e:
        print(f"❌ Error processing {product_name}: {e}")

conn.close()

# --- Save results ---
output_df = pd.DataFrame(results)
output_path = Path(__file__).resolve().parent.parent / "data" / "ai_generated_products.json"
output_df.to_json(output_path, orient="records", indent=2)

print(f"\n✅ Structured JSON saved to {output_path}")
