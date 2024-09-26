# open_ai_backend.py

from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)

# OpenAI Function
def call_openai(some_random_text):
    apiKey = os.getenv("OPEN_AI_API_KEY")
    print(apiKey)

    client = OpenAI(api_key=apiKey)
    
    response = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {
          "role": "system",
          "content": [
            {
              "type": "text",
              "text": some_random_text
            }
          ]
        }
      ],
      temperature=1,
      max_tokens=2048,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      response_format={
        "type": "text"
      }
    )
    
    return response # Assuming the format of response
