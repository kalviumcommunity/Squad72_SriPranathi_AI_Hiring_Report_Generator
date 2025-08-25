import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Config variables
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))
TOP_P = float(os.getenv("TOP_P", 1))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
STOP_SEQUENCE = os.getenv("STOP_SEQUENCE", "###END###")



