from flask import Flask, request, jsonify

from apiResource import generate_response, extract_code  # Import your function
from codeLlama import generate_llama_response, generate_llama_error_response

app = Flask(__name__)


@app.route('/generate_response', methods=['POST'])
def generate_response_endpoint():
    print("Request received at /generate_response")
    data = request.json  # Get JSON data sent by the client
    code_msg = data['code_msg']
    print(code_msg)
    assistant_name = data['assistant_name']
    print(assistant_name)

    try:
        response = generate_response(code_msg, assistant_name)
        print(response)
        return jsonify({'success': True, 'response': response}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/generate_llama_response', methods=['POST'])
def generate_llama_response_call():
    data = request.json
    prompt = data['code_msg']
    print(prompt)
    response = generate_llama_response(prompt)
    response = response.replace("Source: assistant", "")
    response = extract_code(response)
    print(response)
    try:
        return jsonify({'success': True, 'response': response}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/generate_llama_error_response', methods=['POST'])
def generate_llama_error_call():
    data = request.json
    prompt = data['code_msg']
    print(prompt)
    response = generate_llama_error_response(prompt)
    response = response.replace("Source: assistant", "")
    response = extract_code(response)
    try:
        return jsonify({'success': True, 'response': response}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Run the Flask app
