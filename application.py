from flask import Flask, request, jsonify
import torch
import openai
import config
from youtube_transcript_api import YouTubeTranscriptApi

application = Flask(__name__)

#THIS MODULE RETRIEVES THE TRANSCRIPT OF THE YOUTUBE VIDEO
def get_transcript_text(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    transcript_text = ' '.join([entry['text'] for entry in transcript])
    return transcript_text


#THIS MODULE CREATES THE QUIZ
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