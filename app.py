from flask import Flask, request, jsonify
import torch
from transformers import pipeline

app = Flask(__name__)

# LOAD LLM MODEL
model_name = "databricks/dolly-v2-12b"
instruct_pipeline = pipeline(model=model_name, trust_remote_code=True, device_map="auto")


@app.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    print("request received")
    data = request.get_json()

    # Check if the input text is provided
    if 'text' not in data:
        return jsonify({'error': 'Missing text field'}), 400

    input_text = data['text']
    print(f"Input text: {input_text}")
    # Add a prompt to the input text
    prompted_input_text = f"Based on the following text, generate 5 multiple-choice quiz questions and answers: {input_text}"

    # Generate questions using the LLM
    generated_questions = instruct_pipeline(prompted_input_text)
    print("Quiz generation completed")
    
    # Return the generated questions and answers in JSON format
    return jsonify({'questions': generated_questions})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
