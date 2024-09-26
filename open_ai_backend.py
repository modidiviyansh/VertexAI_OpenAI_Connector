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
