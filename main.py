# Entry point and automating all phases of the program
import sys
import subprocess
from pathlib import Path

# Determine the correct Python command based on the operating system
PYTHON_CMD = "python3" if sys.platform == "darwin" else "python"


# -- Define project directories
ROOT_DIR = Path(__file__).resolve().parent
HTML_DIR = ROOT_DIR / "html-export"
AGENTS_DIR = ROOT_DIR / "agents"
DB_DIR = ROOT_DIR / "database"


# -- Phase 1: Data Ingestion
def run_data_ingestion():
    print("📥 PHASE 1: Loading and seeding product data...")
    subprocess.run([PYTHON_CMD, str(DB_DIR / "load_data.py")], check=True)
    print("✅ Data successfully loaded into SQLite database.")
    print(f"\n{'-'*80}\n")

# -- Phase 2: Agent Setup and Content Generation
def run_ai_generation():
    print("🤖 PHASE 2: Generating SEO-optimized content using AI agent...")
    subprocess.run([PYTHON_CMD, str(AGENTS_DIR / "generate_content.py")], check=True)
    print("✅ AI-generated content successfully created and stored.")
    print(f"\n{'-'*80}\n")

# -- Phase 3: HTML Export
def run_html_export():
    print("🌐 PHASE 3: Exporting generated content as static HTML pages...")
    subprocess.run([PYTHON_CMD, str(HTML_DIR / "generate_html.py")], check=True)
    print("✅ HTML pages successfully generated in /html_export directory.")
    print(f"\n{'-'*80}\n")


if __name__ == "__main__":
    print("🚀 Starting A2 Mini Pipeline...")
    try:
        run_data_ingestion()
        run_ai_generation()
        run_html_export()
        print("🎉 All phases completed successfully!")
        print("👉 Preview locally by running:")
        print("   python(3) -m http.server --directory html_export 8080")
        print("   Then visit: http://localhost:8080\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ An error occurred while running the pipeline: {e}")