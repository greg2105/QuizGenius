from flask import Flask, request, jsonify
import torch
import openai
import config
from youtube_transcript_api import YouTubeTranscriptApi

application = app = Flask(__name__)

#THIS MODULE GRABS THE TEXT FROM THE TRANSCRIPT
def get_transcript_text(video_id, start_time, end_time):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return ""

    transcript_text = ""
    for entry in transcript:
        if entry['start'] >= start_time and entry['start'] <= end_time:
            transcript_text += f"{entry['text']} "

    return transcript_text.strip()

#THIS MODULE RETRIEVES THE TRANSCRIPT OF THE YOUTUBE VIDEO
@application.route('/get_transcript', methods=['POST'])
def get_transcript():
    data = request.get_json()

    if 'video_id' not in data or 'start_time' not in data or 'end_time' not in data:
        return jsonify({'error': 'Missing video_id, start_time, or end_time field'}), 400

    video_id = data['video_id']
    start_time = data['start_time']
    end_time = data['end_time']

    transcript_text = get_transcript_text(video_id, start_time, end_time)
    return jsonify({'transcript': transcript_text})

#THIS MODULE CREATES THE QUIZ
openai.api_key = config.chatgpt_api_key
@application.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    print("request received")
    data = {"text": get_transcript.transcript_text}

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
    app.run(host='0.0.0.0', port=5000)