# from flask import Flask, request, jsonify

# app = Flask(__name__)

# @app.route('/prompt/', methods=['POST'])
# def prompt_handler():
#     if request.method == 'POST':
#         data = request.get_json()
#         if not data or 'type' not in data or 'body' not in data:
#             return jsonify({'error': 'Invalid input'}), 400

#         msg = data.get('msg', '')
#         response = prompt_handler(msg)
#         return jsonify({'message': response})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)


# server.py
from model_server import create_app

def initServer():
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
    return app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
