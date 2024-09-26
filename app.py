from flask import Flask, request, jsonify, render_template
from open_ai_backend import call_openai
from vertex_ai_backend import call_vertexai
from response_to_txt_file import clean_and_save_response
import os
import uuid

app = Flask(__name__)

# Directory to store all session data
SESSIONS_DIR = "sessions"

# Create the sessions directory if it doesn't exist
if not os.path.exists(SESSIONS_DIR):
    os.makedirs(SESSIONS_DIR)

# Function to initialize a session with a unique UUID
def init_session():
    session_id = str(uuid.uuid4())  # Generate a unique UUID for the session
    session_dir = os.path.join(SESSIONS_DIR, session_id)
    
    # Create a directory for this session
    os.makedirs(session_dir, exist_ok=True)
    
    # Create empty files for current prompt and last output
    with open(os.path.join(session_dir, "current_prompt.txt"), "w") as f:
        f.write("")
    with open(os.path.join(session_dir, "last_prompt_output.txt"), "w") as f:
        f.write("")
    
    return session_id, session_dir

# Helper function to read content from a file
def read_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            return file.read()
    return ""

# Helper function to write content to a file
def write_file(filepath, content):
    with open(filepath, 'w') as file:
        file.write(content)

# Serve the HTML file
@app.route("/")
def index():
    return render_template("index.html")

# Route to start a new session
@app.route("/start_session", methods=["POST"])
def start_session():
    session_id, session_dir = init_session()
    return jsonify({"session_id": session_id})

# Route to handle user input and model selection
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    model_choice = data.get("model_choice")
    user_input = data.get("user_input")
    session_id = data.get("session_id")

    if not model_choice or not user_input or not session_id:
        return jsonify({"error": "Invalid input or session_id"})

    # Session directory based on session_id
    session_dir = os.path.join(SESSIONS_DIR, session_id)
    if not os.path.exists(session_dir):
        return jsonify({"error": "Invalid session"})

    # File paths for current prompt and last output
    current_prompt_file = os.path.join(session_dir, "current_prompt.txt")
    last_output_file = os.path.join(session_dir, "last_prompt_output.txt")

    # Read the last AI output (from the last_output_file)
    last_output = read_file(last_output_file)

    # Create the full prompt with the user's input and the last output
    prompt_with_context = f"User Input:\n{user_input}\n\nPrevious Output:\n{last_output}"

    # Generate new content based on model choice
    response_text = ""
    if model_choice.lower() == "vertex":
        vertex_ai_op = call_vertexai(prompt_with_context)
        response_text = clean_and_save_response(vertex_ai_op, last_output_file)  # Save to last_output_file
    elif model_choice.lower() == "openai":
        open_ai_op = call_openai(prompt_with_context)
        response_text = clean_and_save_response(open_ai_op, last_output_file)  # Save to last_output_file
    else:
        return jsonify({"error": "Invalid model choice"})

    # Save the current user input to the current_prompt.txt
    write_file(current_prompt_file, user_input)

    return jsonify({"response": response_text})

# Route to end session and delete all session files
@app.route("/end_session", methods=["POST"])
def end_session():
    data = request.json
    session_id = data.get("session_id")

    # Session directory based on session_id
    session_dir = os.path.join(SESSIONS_DIR, session_id)
    
    if os.path.exists(session_dir):
        # Delete the session directory and its contents
        for file in os.listdir(session_dir):
            os.remove(os.path.join(session_dir, file))
        os.rmdir(session_dir)
        return jsonify({"message": f"Session {session_id} ended and files deleted."})
    else:
        return jsonify({"error": "Invalid session"})

if __name__ == "__main__":
    app.run(debug=True)
