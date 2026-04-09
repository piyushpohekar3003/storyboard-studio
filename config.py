import os
from dotenv import load_dotenv

load_dotenv(override=True)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 12000
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "storyboards.db")
