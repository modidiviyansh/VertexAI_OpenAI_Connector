from flask import Flask, request, jsonify
from open_ai_backend import call_openai
from vertex_ai_backend import call_vertexai
from response_to_txt_file import clean_and_save_response

app = Flask(__name__)

# Route to handle user input and model selection
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    model_choice = data.get("model_choice")
    user_input = data.get("user_input")

    if not model_choice or not user_input:
        return jsonify({"error": "Invalid input"})

    # Generate content based on model choice
    response_text = ""
    if model_choice.lower() == "vertex":
        vertex_ai_op = call_vertexai(user_input)
        response_text = clean_and_save_response(vertex_ai_op, "vertex_ai_op.txt")
    elif model_choice.lower() == "openai":
        open_ai_op = call_openai(user_input)
        response_text = clean_and_save_response(open_ai_op, "open_ai_op.txt")
    else:
        return jsonify({"error": "Invalid model choice"})

    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(debug=True)
