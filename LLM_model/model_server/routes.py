# app/routes.py
from flask import Blueprint, request
from .prompt_handler import handle_prompt, background_form

main = Blueprint('main', __name__)

@main.route('/prompt/', methods=['POST'])
def prompt():
    data = request.get_json()
    return handle_prompt(data)

@main.route('/initiateConversation/', methods=['GET'])
def initiateConversation():
    return background_form()


# Test curl req 

# curl http://localhost:5000/initiateConversation

# curl -X POST http://localhost:5000/prompt \
# -H "Content-Type: application/json" \
# -d '{
#   "user_id": "iXQqG",
#   "type": "Form",
#   "body": {
#     "name": "john",
#     "age": "20",
#     "gender": "Male",
#     "previous_disease": "None",
#     "allergies": "None"
#   }
# }'

