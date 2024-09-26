# vertex_ai_backend.py

import base64
import vertexai
from vertexai.preview.generative_models import GenerativeModel, SafetySetting, Tool
from vertexai.preview.generative_models import grounding

# Vertex AI Function
def call_vertexai(prompt_text):
    vertexai.init(project="266253766187", location="us-central1")
    tools = [
        Tool.from_google_search_retrieval(
            google_search_retrieval=grounding.GoogleSearchRetrieval()
        ),
    ]
    model = GenerativeModel(
        "projects/266253766187/locations/us-central1/endpoints/525725987262955520",
        tools=tools,
    )
    chat = model.start_chat()

    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 1,
        "top_p": 1,
    }

    safety_settings = [
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
    ]

    response = chat.send_message(
        [prompt_text],
        generation_config=generation_config,
        safety_settings=safety_settings
    )

    return response  # Assuming the format of response


def clean_and_save_vertexai_response(response, file_path="vertexai_output.txt"):
    # Extract the relevant part of the response
    try:
        # Accessing attributes instead of subscripting
        cleaned_text = response.candidates[0].content.parts[0].text
    except (AttributeError, IndexError):
        print("Error extracting text from Vertex AI response")
        cleaned_text = ""

    # Save the cleaned text to a .txt file
    with open(file_path, 'w') as f:
        f.write(cleaned_text)

    print(f"Cleaned Vertex AI response saved to {file_path}")