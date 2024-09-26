def clean_and_save_response(response, file_path):
    """
    Automatically detects whether the response is from Vertex AI or OpenAI,
    extracts the relevant text, and saves it to a .txt file.
    
    Args:
    - response: The API response from either Vertex AI or OpenAI.
    - file_path: The path where the cleaned text will be saved.
    
    Returns:
    - cleaned_text: The extracted and cleaned text from the AI response.
    """
    cleaned_text = ""

    # Try to extract text from a Vertex AI response
    try:
        # Vertex AI usually returns candidates, content, and parts
        cleaned_text = response.candidates[0].content.parts[0].text
        print("Vertex AI response detected.")
    except (AttributeError, IndexError):
        # If Vertex AI extraction fails, continue to check for OpenAI response
        pass

    # Try to extract text from an OpenAI response
    if not cleaned_text:
        try:
            # OpenAI returns choices, message, and content
            cleaned_text = response['choices'][0]['message']['content']
            print("OpenAI response detected.")
        except (KeyError, IndexError):
            # Handle unrecognized response format with an error message
            print("Error: Unrecognized response format.")
            return ""

    # Save the cleaned text to a .txt file if it was successfully extracted
    if cleaned_text:
        with open(file_path, 'w') as f:
            f.write(cleaned_text)
        print(f"Cleaned response saved to {file_path}")
    else:
        print(f"No content to save from the response for {file_path}")

    return cleaned_text
