from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/prompt/', methods=['POST'])
def prompt_handler():
    if request.method == 'POST':
        data = request.get_json()
        msg = data.get('msg', '')
        response = prompt_handler(msg)
        return jsonify({'message': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
