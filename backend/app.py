from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/parse', methods=['POST'])
def parse_solidity():
    """
    Endpoint to receive Solidity code and return CFG data
    The actual parsing will be done on the frontend using @solidity-parser/parser
    This endpoint can be extended for additional backend processing if needed
    """
    try:
        data = request.get_json()
        solidity_code = data.get('code', '')
        
        # For now, this endpoint validates the request
        # The CFG generation will happen on the frontend
        if not solidity_code:
            return jsonify({'error': 'No code provided'}), 400
        
        return jsonify({
            'status': 'success',
            'message': 'Code received successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
