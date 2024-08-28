import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)