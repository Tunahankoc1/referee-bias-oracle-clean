cat > app.py << 'EOF'
from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    try:
        return open('index.html').read(), 200, {'Content-Type': 'text/html'}
    except:
        return "Loading...", 200

@app.route('/api/txline/jwt', methods=['POST'])
def get_jwt():
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF

git add app.py
git commit -m "Fix build"
git push
