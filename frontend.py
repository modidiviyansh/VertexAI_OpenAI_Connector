from open_ai_backend import call_openai
from vertex_ai_backend import call_vertexai
from response_to_txt_file import clean_and_save_response

print("Imports are successful")

# Example usage
initial_input = "Write a blog about Digital Marketing trends in 2024."

# Calling Vertex AI backend
print("Calling Vertex AI...")
vertex_ai_op = call_vertexai(initial_input)
print("Vertex AI Response: ", vertex_ai_op)
file_path_vertex = "vertex_ai_op.txt";
    
clean_and_save_response(vertex_ai_op,file_path_vertex)


# Calling OpenAI backend
print("Calling OpenAI...")
open_ai_op = call_openai(initial_input)
print("OpenAI Response: ", open_ai_op)
file_path_openai = "open_ai_op.txt";
clean_and_save_response(open_ai_op,file_path_openai)
