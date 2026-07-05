from flask import Flask, send_from_directory, jsonify
import requests
import os

app = Flask(__name__, static_folder='.', static_url_path='')

TXLINE_API = "https://txline-dev.txodds.com"

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/api/txline/fixtures')
def get_fixtures():
    try:
        auth_res = requests.post(f"{TXLINE_API}/auth/guest/start", timeout=10)
        jwt_token = auth_res.json().get('token')
        
        if not jwt_token:
            return jsonify({'error': 'JWT failed'}), 500
        
        fixtures_res = requests.get(
            f"{TXLINE_API}/api/fixtures",
            headers={'Authorization': f'Bearer {jwt_token}'},
            params={'league': 'WORLD_CUP'},
            timeout=10
        )
        
        fixtures = fixtures_res.json() if fixtures_res.status_code == 200 else []
        return jsonify({'success': True, 'fixtures': fixtures[:20]})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
