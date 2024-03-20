from flask import Flask, request, jsonify
import json
import os

from apiResource import generate_response  # Import your function
from codeLlama import generate_LLama_response

app = Flask(__name__)


@app.route('/generate_response', methods=['POST'])
def generate_response_endpoint():
    data = request.json  # Get JSON data sent by the client
    code_msg = data['code_msg']
    assistant_name = data['assistant_name']

    try:
        response = generate_response(code_msg, assistant_name)
        return jsonify({'success': True, 'response': response}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/generate_llama_response', methods=['POST'])
def generate_llama_response():
    data = request.json
    prompt = data['prompt']
    print(prompt)
    response = generate_LLama_response(prompt)
    try:
        return jsonify({'success': True, 'response': response}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Run the Flask app
