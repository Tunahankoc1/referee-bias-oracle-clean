@app.route('/api/txline/fixtures')
def get_fixtures():
    try:
        # Login
        auth_res = requests.post(
            "https://worldcup26.ir/auth/authenticate",
            json={"email": "referee@oracle.com", "password": "oracle123"},
            timeout=10
        )
        token = auth_res.json().get('token')
        
        if not token:
            return jsonify({'error': 'Auth failed', 'fixtures': []}), 500
        
        # Get games
        games_res = requests.get(
            "https://worldcup26.ir/get/games",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        
        games = games_res.json().get('games', [])
        
        # Format
        fixtures = []
        for g in games[:20]:
            fixtures.append({
                'home_team': g.get('home_team_name_en', 'TBD'),
                'away_team': g.get('away_team_name_en', 'TBD'),
                'home_score': g.get('home_score', '0'),
                'away_score': g.get('away_score', '0'),
                'status': g.get('time_elapsed', 'scheduled'),
                'date': g.get('local_date', 'TBA'),
                'group': g.get('group', '')
            })
        
        return jsonify({'success': True, 'fixtures': fixtures, 'source': 'WorldCup26 Live'})
        
    except Exception as e:
        return jsonify({'error': str(e), 'fixtures': []}), 500
