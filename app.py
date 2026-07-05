import os

@app.route('/api/txline/fixtures')
def get_fixtures():
    try:
        api_token = os.environ.get('TXLINE_API_TOKEN') or os.environ.get('txline_api_token')
        
        if not api_token:
            return jsonify({'error': 'No API token', 'fixtures': []}), 500
        
        fixtures_res = requests.get(
            "https://txline-dev.txodds.com/api/fixtures",
            headers={
                'Authorization': f'Bearer {api_token}',
                'Accept-Encoding': 'gzip, deflate',
                'User-Agent': 'Mozilla/5.0'
            },
            params={'league': 'WORLD_CUP'},
            timeout=10
        )
        
        if fixtures_res.status_code == 200:
            fixtures = fixtures_res.json()
            return jsonify({'success': True, 'fixtures': fixtures[:20], 'source': 'TxLINE Live'})
        else:
            return jsonify({'error': f'API error: {fixtures_res.status_code}', 'fixtures': []}), 500
            
    except Exception as e:
        return jsonify({'error': str(e), 'fixtures': []}), 500
