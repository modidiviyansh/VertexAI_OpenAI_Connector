def clean_and_save_response(response, file_path):
    """
    This function automatically detects whether the response is from Vertex AI or OpenAI,
    extracts the relevant text, and saves it to a .txt file.
    """
    cleaned_text = ""

    # Try to extract from Vertex AI format (dot notation access)
    try:
        # If it's a Vertex AI response, we should find candidates and content
        cleaned_text = response.candidates[0].content.parts[0].text
        print("Vertex AI response detected")
    except (AttributeError, IndexError):
        # If Vertex AI extraction fails, move on to check for OpenAI response structure
        pass

    # Try to extract from OpenAI format (dot notation access)
    if not cleaned_text:
        try:
            # OpenAI's ChatCompletion object has attributes, not dictionary keys
            cleaned_text = response.choices[0].message.content
            print("OpenAI response detected")
        except (AttributeError, IndexError):
            # If neither format works, raise an error or return an empty string
            print("Error: Unrecognized response format")

    # Save the cleaned text to a .txt file
    with open(file_path, 'w') as f:
        f.write(cleaned_text)

    print(f"Cleaned response saved to {file_path}")

    return cleaned_text
