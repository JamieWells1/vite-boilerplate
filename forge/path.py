from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / ".env"
ENV_EXAMPLE_PATH = BASE_DIR / ".env.example"
TW_CONFIG_PATH = BASE_DIR / "tailwind.config.js"
INDEX_CSS_PATH = BASE_DIR / "src" / "index.css"
FORGE_CONFIG_PATH = BASE_DIR / "forge.config.json"
