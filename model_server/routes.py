# app/routes.py
from flask import Blueprint, request
from .prompt_handler import handle_prompt

main = Blueprint('main', __name__)

@main.route('/prompt/', methods=['POST'])
def prompt():
    data = request.get_json()
    return handle_prompt(data)
