import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if len(sys.argv) != 2:
  print("Usage: python3 main.py <content>")
  sys.exit(1)

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
  model="gemini-2.0-flash-001", 
  contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
)

print(response.text)
print("Prompt tokens:", response.usage_metadata.prompt_token_count)
print("Response tokens:", response.usage_metadata.candidates_token_count)