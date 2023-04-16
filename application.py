from flask import Flask, request, jsonify
import torch
import openai
import config

application = Flask(__name__)

# LOAD LLM MODEL
openai.api_key = config.chatgpt_api_key

@application.route('/generate_quiz', methods=['POST'])
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

    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
        {"role": "user", "content" : prompted_input_text}
        ]
    )

    # Generate questions using the LLM
    generated_questions = completion.choices[0].message.content
    print("Quiz generation completed")
    
    # Return the generated questions and answers in JSON format
    return jsonify({'questions': generated_questions})

if __name__ == '__main__':
    application.run()