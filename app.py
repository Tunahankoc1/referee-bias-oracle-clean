from flask import Flask, jsonify
import requests
import json

app = Flask(__name__)
TXLINE_API = "https://txline-dev.txodds.com"

@app.route('/api/txline/fixtures')
def get_fixtures():
    try:
        # Get guest JWT
        auth_res = requests.post(
            f"{TXLINE_API}/auth/guest/start",
            timeout=10,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        jwt_data = auth_res.json()
        jwt_token = jwt_data.get('token')
        
        if not jwt_token:
            return jsonify({'error': 'JWT failed'}), 500
        
        # Get fixtures WITH compression handling
        fixtures_res = requests.get(
            f"{TXLINE_API}/api/fixtures",
            headers={
                'Authorization': f'Bearer {jwt_token}',
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'application/json'
            },
            params={'league': 'WORLD_CUP'},
            timeout=10
        )
        
        if fixtures_res.status_code != 200:
            return jsonify({'error': f'API returned {fixtures_res.status_code}'}), 500
        
        try:
            fixtures = fixtures_res.json()
        except:
            # Raw text döndüyse parse et
            fixtures = json.loads(fixtures_res.text)
        
        return jsonify({'success': True, 'fixtures': fixtures[:20]})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
