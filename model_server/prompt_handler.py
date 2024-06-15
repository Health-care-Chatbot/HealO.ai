# app/controllers.py
from flask import jsonify

def text_prompt_handler(msg):
    

def handle_prompt(data):
    if not data or 'type' not in data or 'body' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    response = {}

    # Handle the different types of input
    if data['type'] == 'Text':
        resp = text_prompt_handler(data['body'])
        response['type'] = 'Text'
        response['body'] = resp
    elif data['type'] == 'Form':
        if not isinstance(data['body'], dict):
            return jsonify({'error': 'Invalid form data'}), 400
        response['message'] = 'Form'
        response['body'] = data['body']
    else:
        return jsonify({'error': 'Unknown type'}), 400

    return jsonify(response), 200
