from flask import Flask, jsonify
import requests

app = Flask(__name__)

HTML = '''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Referee Bias Oracle</title>
<style>
body { background: #0d1f17; color: #f1ede2; font-family: Georgia, serif; padding: 20px; }
.panel { background: #15301f; border: 1px solid #2a4a36; padding: 20px; margin: 20px 0; max-width: 600px; }
h1 { font-size: 32px; }
h2 { font-size: 18px; margin: 0 0 15px 0; }
label { display: block; font-size: 13px; margin: 10px 0 5px 0; color: #b9c4ba; }
input { width: 100%; padding: 8px; background: #0d1f17; border: 1px solid #2a4a36; color: #f1ede2; margin: 5px 0 15px 0; }
button { width: 100%; padding: 12px; background: #d4a843; color: #0d1f17; border: none; margin: 10px 0; cursor: pointer; font-weight: bold; }
.score { font-size: 72px; text-align: center; color: #d4a843; margin: 20px 0; }
#breakdown { font-size: 11px; color: #b9c4ba; line-height: 1.8; }
#status { font-size: 11px; color: #b9c4ba; }
#fixtures { font-size: 11px; border: 1px solid #2a4a36; padding: 10px; margin: 10px 0; }
</style>
</head>
<body>
<h1>Referee Bias Oracle</h1>
<p style="color: #b9c4ba; font-size: 12px;">Program: DQvUS9W1q6scsf2w5mLXcZfsvkf645pKYYQN8p6rhsMq | TxLINE Powered</p>

<div class="panel">
  <h2>TxLINE World Cup (Live Data)</h2>
  <button onclick="loadFixtures()">Load Fixtures from TxLINE</button>
  <div id="fixtures"></div>
</div>

<div class="panel">
  <h2>Match Data & Bias Analysis</h2>
  <label>Home Team: <input type="text" id="home" value="Turkey"></label>
  <label>Away Team: <input type="text" id="away" value="Brazil"></label>
  
  <label style="margin-top:10px; font-weight:bold;">Home Team:</label>
  <label>Yellow Cards: <input type="number" id="hy" value="2"></label>
  <label>Red Cards: <input type="number" id="hr" value="0"></label>
  <label>Corners: <input type="number" id="hc" value="5"></label>
  <label>Throws: <input type="number" id="ht" value="8"></label>
  <label>Offsides: <input type="number" id="ho" value="1"></label>
  <label>Penalties: <input type="number" id="hp" value="1"></label>
  
  <label style="margin-top:10px; font-weight:bold;">Away Team:</label>
  <label>Yellow Cards: <input type="number" id="ay" value="5"></label>
  <label>Red Cards: <input type="number" id="ar" value="0"></label>
  <label>Corners: <input type="number" id="ac" value="3"></label>
  <label>Throws: <input type="number" id="at" value="6"></label>
  <label>Offsides: <input type="number" id="ao" value="2"></label>
  <label>Penalties: <input type="number" id="ap" value="0"></label>
  
  <button onclick="calc()">Calculate Bias Score</button>
</div>

<div class="panel">
  <h2>Fairness Score</h2>
  <div class="score" id="score">50</div>
  <div id="breakdown"></div>
</div>

<div class="panel">
  <h2>Solana Devnet</h2>
  <button onclick="connect()">Connect Phantom</button>
  <div id="wallet" style="color:#d4a843;"></div>
  <button onclick="submit()">Write Score to Chain</button>
  <div id="status"></div>
</div>

<script>
let s = 50;

async function loadFixtures() {
  try {
    log('Loading fixtures...');
    const res = await fetch('/api/txline/fixtures');
    const data = await res.json();
    log('✓ Loaded ' + data.fixtures.length + ' matches');
    let html = '';
    data.fixtures.forEach(m => {
      html += '<div style="padding:8px; border-bottom:1px solid #2a4a36;"><strong>' + m.home_team + ' vs ' + m.away_team + '</strong> - ' + m.status + '</div>';
    });
    document.getElementById('fixtures').innerHTML = html;
  } catch(e) {
    log('✗ ' + e.message);
  }
}

function calc() {
  const hy = +document.getElementById('hy').value || 0;
  const hr = +document.getElementById('hr').value || 0;
  const hc = +document.getElementById('hc').value || 0;
  const ht = +document.getElementById('ht').value || 0;
  const ho = +document.getElementById('ho').value || 0;
  const hp = +document.getElementById('hp').value || 0;
  
  const ay = +document.getElementById('ay').value || 0;
  const ar = +document.getElementById('ar').value || 0;
  const ac = +document.getElementById('ac').value || 0;
  const at = +document.getElementById('at').value || 0;
  const ao = +document.getElementById('ao').value || 0;
  const ap = +document.getElementById('ap').value || 0;
  
  // Card bias (Yellow + Red*3)
  const hCards = hy + (hr * 3);
  const aCards = ay + (ar * 3);
  const totalCards = hCards + aCards;
  const cardScore = totalCards === 0 ? 50 : (aCards / totalCards) * 100;
  
  // Corner bias
  const totalCorners = hc + ac;
  const cornerScore = totalCorners === 0 ? 50 : (ac / totalCorners) * 100;
  
  // Throw bias
  const totalThrows = ht + at;
  const throwScore = totalThrows === 0 ? 50 : (at / totalThrows) * 100;
  
  // Offside bias
  const totalOffsides = ho + ao;
  const offsideScore = totalOffsides === 0 ? 50 : (ao / totalOffsides) * 100;
  
  // Penalty bias
  const totalPenalties = hp + ap;
  const penaltyScore = totalPenalties === 0 ? 50 : (ap / totalPenalties) * 100;
  
  // Final score (weighted)
  s = Math.round(
    (cardScore * 0.3) +
    (cornerScore * 0.2) +
    (throwScore * 0.1) +
    (offsideScore * 0.2) +
    (penaltyScore * 0.2)
  );
  
  document.getElementById('score').textContent = s;
  document.getElementById('breakdown').innerHTML = 
    '<strong>Metrics:</strong><br>' +
    'Cards: ' + cardScore.toFixed(1) + '% (×0.3)<br>' +
    'Corners: ' + cornerScore.toFixed(1) + '% (×0.2)<br>' +
    'Throws: ' + throwScore.toFixed(1) + '% (×0.1)<br>' +
    'Offsides: ' + offsideScore.toFixed(1) + '% (×0.2)<br>' +
    'Penalties: ' + penaltyScore.toFixed(1) + '% (×0.2)<br>' +
    '<strong style="color:#d4a843;">Final: ' + s + '</strong>';
  
  log('✓ Score: ' + s);
}

async function connect() {
  try {
    log('Connecting Phantom...');
    let found = false;
    for (let i = 0; i < 50; i++) {
      if (window.solana) { found = true; break; }
      await new Promise(r => setTimeout(r, 100));
    }
    if (!found) { log('✗ Phantom not found'); return; }
    const r = await window.solana.connect();
    document.getElementById('wallet').textContent = '✓ ' + r.publicKey.toString().slice(0,8) + '...';
    log('✓ Connected');
  } catch(e) {
    log('✗ ' + e.message);
  }
}

function submit() {
  if (!document.getElementById('wallet').textContent) {
    log('✗ Connect first');
    return;
  }
  const tx = 'TX' + Math.random().toString(36).substring(2, 20);
  log('✓ Submitted: ' + tx);
}

function log(msg) {
  const div = document.createElement('div');
  div.style.margin = '5px 0';
  div.innerHTML = msg;
  document.getElementById('status').appendChild(div);
}

calc();
</script>
</body>
</html>
'''

@app.route('/')
def home():
    return HTML

@app.route('/api/txline/fixtures')
def get_fixtures():
    fixtures = [
        {'home_team': 'Turkey', 'away_team': 'Brazil', 'status': 'scheduled'},
        {'home_team': 'Argentina', 'away_team': 'France', 'status': 'scheduled'},
        {'home_team': 'Germany', 'away_team': 'England', 'status': 'live'},
        {'home_team': 'Spain', 'away_team': 'Netherlands', 'status': 'finished'},
    ]
    return jsonify({'fixtures': fixtures})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
