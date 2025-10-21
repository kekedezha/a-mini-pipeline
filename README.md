# 🧠 A Mini Pipeline

A lightweight end-to-end demo inspired by **A2 Analytics’ AI-powered SEO workflow**.  
This project showcases how to transform raw structured data into optimized, publish-ready web content — fast.

## 🚀 Overview

This pipeline simulates how A2 Analytics builds data-driven SEO content at scale:

1. **Data Ingestion** → Load and clean structured data (CSV → SQLite database).
2. **AI Content Generation** → Use a LangChain-powered AI agent to create SEO-friendly meta titles, descriptions, and product blurbs.
3. **HTML Publishing** → Automatically generate static HTML pages (with meta tags) using Jinja2 templates for SEO deployment.
4. **Index Page** → Build an `index.html` linking to all generated pages for a quick demo of your “live” output.

## 🏗️ Project Structure

```bash
a2-mini-pipeline/
├── README.md
├── agents
│   ├── generate_content.py
│   └── prompts
│       └── product_prompt.txt
├── data
│   ├── ai_generated_products.json
│   └── raw_products.csv
├── database
│   ├── a2_pipeline.db
│   └── load_data.py
├── html-export
│   ├── airbuds_lite.html
│   ├── aircool_breeze.html
│   ├── fitband_3.html
│   ├── generate_html.py
│   ├── homeguard_pro.html
│   ├── index.html
│   ├── photosnap_x.html
│   ├── smartlamp_x10.html
│   ├── soundbeam_mini.html
│   ├── sounddock_2.html
│   ├── templates
│   │   └── product_template.html
│   ├── tempsmart_kettle.html
│   └── workmate_keyboard.html
├── main.py
├── requirements.txt
└── tests
    └── test_database_load.py
```

## 🧩 How It Works

### 1️⃣ Data Ingestion

```bash
python3 database/load_data.py
```

- Reads products.csv
- Creates a2_pipeline.db
- Stores each product as a row in a products table

### 2️⃣ AI Content Generation

```bash
python3 agents/generate_content.py
```

- Pulls data from SQLite
- Sends each product's details to an **AI Agent** (via LangChain + OpenAI)
- The model generates:
  - meta_title
  - meta_description
  - product_description
- Saves structured JSON to /data/ai_generated_products.json

### 3️⃣ AI Content Generation

```bash
python3 html-export/generate_html.py
```

- Reads the AI output JSON
- Uses **Jinja2** to render SEO-optimized HTML pages
- Creates:
  - One HTML file per product
  - an index.html that links them all together

### 🌐 Preview Locally

To preview the generated pages locally:

```bash
python -m http.server --directory html_export 8080
```

## 💡 Tech Stack

- Python 3.11+
- LangChain — LLM orchestration and prompt management
- OpenAI GPT-4o-mini — AI content generation
- SQLite3 — Local structured data store
- Jinja2 — HTML template rendering
- dotenv — Environment variable management

## 🔑 Environment Variables

Create a .env file in the project root:

```bash
OPENAI_API_KEY=your_api_key_here
```

## 🧭 Future Improvements

- Add async parallelization for faster AI generation
- Implement response caching to avoid duplicate calls
- Build a FastAPI layer to serve generated pages dynamically
- Integrate LangGraph for multi-agent collaboration

## 👨‍💻 Author

Christian Dezha
AI + Full Stack Engineer — Charlotte, NC

Built this project as a hands-on exploration of A2 Analytics’ approach to scalable, AI-powered SEO systems.
