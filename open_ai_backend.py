# open_ai_backend.py

from openai import OpenAI

# OpenAI Function
def call_openai(some_random_text):
    client = OpenAI(api_key="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")
    
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
