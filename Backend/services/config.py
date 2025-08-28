import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Config variables
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))
TOP_P = float(os.getenv("TOP_P", 1))
TOP_K = int(os.getenv("TOP_K", 50))

STOP_SEQUENCE = os.getenv("STOP_SEQUENCE", "###END###")



