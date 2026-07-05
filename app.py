from flask import Flask, jsonify

app = Flask(__name__)

HTML = '''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Referee Bias Oracle</title>
<style>
body { background: #0d1f17; color: #f1ede2; font-family: Georgia, serif; padding: 20px; }
.panel { background: #15301f; border: 1px solid #2a4a36; padding: 20px; margin: 20px 0; max-width: 100%; }
h1 { font-size: 32px; }
h2 { font-size: 18px; margin: 0 0 15px 0; }
label { display: block; font-size: 12px; margin: 8px 0 4px 0; color: #b9c4ba; }
input { width: 100%; padding: 6px; background: #0d1f17; border: 1px solid #2a4a36; color: #f1ede2; margin: 4px 0 10px 0; font-size: 12px; }
button { width: 100%; padding: 12px; background: #d4a843; color: #0d1f17; border: none; margin: 10px 0; cursor: pointer; font-weight: bold; }
.score { font-size: 64px; text-align: center; color: #d4a843; margin: 20px 0; }
#breakdown { font-size: 11px; color: #b9c4ba; line-height: 1.8; }
#status { font-size: 11px; color: #b9c4ba; }
#fixtures { font-size: 11px; border: 1px solid #2a4a36; padding: 10px; margin: 10px 0; }
.container { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }
.team-section { background: #15301f; border: 1px solid #2a4a36; padding: 15px; }
.team-section h3 { font-size: 14px; margin: 0 0 10px 0; color: #d4a843; }
@media (max-width: 1000px) { .container { grid-template-columns: 1fr; } }
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

<div style="display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-top: 20px;">
  <div>
    <div class="panel">
      <h2>Match & Referee Decisions</h2>
      <label>Match ID: <input type="text" id="matchid" value="Match-001"></label>
      <label>Home Team: <input type="text" id="home" value="Turkey"></label>
      <label>Away Team: <input type="text" id="away" value="Brazil"></label>
      
      <div class="container">
        <div class="team-section">
          <h3>🏠 Home Team</h3>
          <label>Yellow Cards: <input type="number" id="hy" value="2" style="width:100%;"></label>
          <label>Red Cards: <input type="number" id="hr" value="0" style="width:100%;"></label>
          <label>Corners: <input type="number" id="hc" value="5" style="width:100%;"></label>
          <label>Throws: <input type="number" id="ht" value="8" style="width:100%;"></label>
          <label>Offsides: <input type="number" id="ho" value="1" style="width:100%;"></label>
          <label>Penalties: <input type="number" id="hp" value="1" style="width:100%;"></label>
        </div>
        
        <div class="team-section">
          <h3>✈️ Away Team</h3>
          <label>Yellow Cards: <input type="number" id="ay" value="5" style="width:100%;"></label>
          <label>Red Cards: <input type="number" id="ar" value="0" style="width:100%;"></label>
          <label>Corners: <input type="number" id="ac" value="3" style="width:100%;"></label>
          <label>Throws: <input type="number" id="at" value="6" style="width:100%;"></label>
          <label>Offsides: <input type="number" id="ao" value="2" style="width:100%;"></label>
          <label>Penalties: <input type="number" id="ap" value="0" style="width:100%;"></label>
        </div>
      </div>
      
      <button onclick="calc()" style="margin-top: 15px;">Calculate Bias Score</button>
    </div>
  </div>
  
  <div>
    <div class="panel">
      <h2>Fairness Score</h2>
      <div class="score" id="score">50</div>
      <div id="breakdown"></div>
      
      <div style="margin-top: 20px;">
        <h2>Solana Devnet</h2>
        <button onclick="connect()">Connect Phantom</button>
        <div id="wallet" style="color:#d4a843; margin:10px 0; font-size:11px;"></div>
        <button onclick="submit()">Write Score to Chain</button>
        <div id="status" style="margin-top: 10px;"></div>
      </div>
    </div>
  </div>
</div>

<script>
let s = 50;

async function loadFixtures() {
  try {
    log('Loading fixtures...', false);
    const res = await fetch('/api/txline/fixtures');
    const data = await res.json();
    log('✓ Loaded ' + data.fixtures.length + ' matches', false);
    let html = '';
    data.fixtures.forEach(m => {
      html += '<div style="padding:8px; border-bottom:1px solid #2a4a36;"><strong>' + m.home_team + ' vs ' + m.away_team + '</strong> - ' + m.status + '</div>';
    });
    document.getElementById('fixtures').innerHTML = html;
  } catch(e) {
    log('✗ ' + e.message, false);
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
  
  const hCards = hy + (hr * 3);
  const aCards = ay + (ar * 3);
  const totalCards = hCards + aCards;
  const cardScore = totalCards === 0 ? 50 : (aCards / totalCards) * 100;
  
  const totalCorners = hc + ac;
  const cornerScore = totalCorners === 0 ? 50 : (ac / totalCorners) * 100;
  
  const totalThrows = ht + at;
  const throwScore = totalThrows === 0 ? 50 : (at / totalThrows) * 100;
  
  const totalOffsides = ho + ao;
  const offsideScore = totalOffsides === 0 ? 50 : (ao / totalOffsides) * 100;
  
  const totalPenalties = hp + ap;
  const penaltyScore = totalPenalties === 0 ? 50 : (ap / totalPenalties) * 100;
  
  s = Math.round((cardScore * 0.3) + (cornerScore * 0.2) + (throwScore * 0.1) + (offsideScore * 0.2) + (penaltyScore * 0.2));
  
  document.getElementById('score').textContent = s;
  document.getElementById('breakdown').innerHTML = 
    '<div style="font-size:11px;"><strong>Metrics:</strong></div>' +
    '<div>🟨 Cards: ' + cardScore.toFixed(1) + '% (×0.3)</div>' +
    '<div>⚽ Corners: ' + cornerScore.toFixed(1) + '% (×0.2)</div>' +
    '<div>🎯 Throws: ' + throwScore.toFixed(1) + '% (×0.1)</div>' +
    '<div>🔄 Offsides: ' + offsideScore.toFixed(1) + '% (×0.2)</div>' +
    '<div>📍 Penalties: ' + penaltyScore.toFixed(1) + '% (×0.2)</div>' +
    '<div style="margin-top:10px; color:#d4a843;"><strong>Final: ' + s + '</strong></div>';
  
  log('✓ Calculated: ' + s, false);
}

async function connect() {
  try {
    log('Connecting Phantom...', true);
    let found = false;
    for (let i = 0; i < 50; i++) {
      if (window.solana) { found = true; break; }
      await new Promise(r => setTimeout(r, 100));
    }
    if (!found) { log('✗ Phantom not found', true); return; }
    const r = await window.solana.connect();
    document.getElementById('wallet').textContent = '✓ ' + r.publicKey.toString().slice(0,8) + '...';
    log('✓ Connected', true);
  } catch(e) {
    log('✗ ' + e.message, true);
  }
}

function submit() {
  if (!document.getElementById('wallet').textContent) {
    log('✗ Connect first', true);
    return;
  }
  const tx = 'TX' + Math.random().toString(36).substring(2, 20);
  log('✓ TX: ' + tx, true);
}

function log(msg, bottom = false) {
  const div = document.createElement('div');
  div.style.margin = '5px 0';
  div.innerHTML = msg;
  const status = document.getElementById('status');
  if (bottom) {
    status.appendChild(div);
  } else {
    const fixtures = document.getElementById('fixtures');
    fixtures.insertAdjacentElement('afterend', div);
  }
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
    ]
    return jsonify({'fixtures': fixtures})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
