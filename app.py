from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

TXLINE_API = "https://txline-dev.txodds.com"

@app.route('/')
def home():
    return open('index.html').read(), 200, {'Content-Type': 'text/html'}

@app.route('/api/txline/jwt', methods=['POST'])
def get_jwt():
    try:
        res = requests.post(f"{TXLINE_API}/auth/guest/start", timeout=5)
        if res.status_code == 200:
            return jsonify({'success': True, 'data': res.json()})
        return jsonify({'error': 'JWT failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
