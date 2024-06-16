# app/controllers.py
from flask import jsonify
from main import *
import random
import string
from LLM_controllers import get_llm_response, set_background_form, get_background_form



def get_random_5_letter_user_id():
    return ''.join(random.choices(string.ascii_letters, k=5))

def background_form():
    user_id = get_random_5_letter_user_id()
    response = {
        "user_id": user_id,
        "conversation": [
            {
                "type": "Text",
                "body": "Hey there! I am Healo, your family medical consultant"
            },
            {
                "type": "Form",
                "body": {
                    "name": "",
                    "age": "",
                    "gender": "",
                    "previous_disease": "",
                    "allergies": ""
                }
            },
            {
                "type": "Text",
                "body": "Please fill out the form above so that I can assist you better."
            },
        ]
    }
    return jsonify(response), 200

def text_prompt_handler(user_id, msg):
    output =  get_llm_response(user_id, msg, get_background_form())
    response = {
        "user_id": user_id,
        "conversation": [
            {
                "type": "Text",
                "body": output
            },
        ]
    }
    return response

def form_prompt_handler(user_id, form_data):
    global background
    
    body_string = json.dumps(form_data)
    set_background_form(body_string)
    response = {
        "user_id": user_id,
        "conversation": [
            {
                "type": "Text",
                "body": "Thank you. Can you please provide me with your symptoms"
            },
        ]
    }
    return response

def handle_prompt(data):
    if not data or 'user_id' not in data or 'type' not in data or 'body' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    response = {}
    user_id = data['user_id']
    if(user_id == ''):
        user_id = "HealO"
    # Handle the different types of input
    if data['type'] == 'Text':
        resp = text_prompt_handler(user_id, data['body'])
        # response['type'] = 'Text'
        response = resp
    elif data['type'] == 'Form':
        if not isinstance(data['body'], dict):
            return jsonify({'error': 'Invalid form data'}), 400
        resp = form_prompt_handler(user_id, json.dumps(data['body']))
        # response['type'] = 'Form'
        response = resp
    else:
        return jsonify({'error': 'Unknown type'}), 400

    return jsonify(response), 200
