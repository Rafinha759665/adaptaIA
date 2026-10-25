import os

from dotenv import load_dotenv


load_dotenv()


GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)