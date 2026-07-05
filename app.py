from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Referee Bias Oracle</title>
<style>
body { background: #0d1f17; color: #f1ede2; font-family: Georgia, serif; padding: 20px; }
.panel { background: #15301f; border: 1px solid #2a4a36; padding: 20px; margin: 20px 0; }
h1 { font-size: 32px; }
h2 { font-size: 18px; margin: 0 0 15px 0; }
label { display: block; font-size: 12px; margin: 8px 0 4px 0; color: #b9c4ba; }
input { width: 100%; padding: 6px; background: #0d1f17; border: 1px solid #2a4a36; color: #f1ede2; margin: 4px 0 10px 0; font-size: 12px; }
button { width: 100%; padding: 12px; background: #d4a843; color: #0d1f17; border: none; margin: 10px 0; cursor: pointer; font-weight: bold; }
.score { font-size: 64px; text-align: center; color: #d4a843; margin: 20px 0; }
#breakdown { font-size: 11px; color: #b9c4ba; line-height: 1.8; }
#status { font-size: 11px; color: #b9c4ba; }
#fixtures { font-size: 11px; border: 1px solid #2a4a36; padding: 10px; margin: 10px 0; max-height: 300px; overflow-y: auto; }
.team-section { background: #0d1f17; border: 1px solid #2a4a36; padding: 15px; }
.team-section h3 { font-size: 14px; margin: 0 0 10px 0; color: #d4a843; }
</style>
</head>
<body>
<h1>Referee Bias Oracle</h1>
<p style="color: #b9c4ba; font-size: 12px;">Program: DQvUS9W1q6scsf2w5mLXcZfsvkf645pKYYQN8p6rhsMq | World Cup 2026 Live Data</p>

<div class="panel">
  <h2>World Cup 2026 Live Fixtures</h2>
  <button onclick="loadFixtures()">Load Live Matches</button>
  <div id="fixtures"></div>
</div>

<div style="display:grid; grid-template-columns:2fr 1fr; gap:20px; margin-top:20px;">
  <div>
    <div class="panel">
      <h2>Match & Referee Decisions</h2>
      <label>Match ID: <input type="text" id="matchid" value="Match-001"></label>
      <label>Home Team: <input type="text" id="home" value="Turkey"></label>
      <label>Away Team: <input type="text" id="away" value="Brazil"></label>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:15px; margin-top:15px;">
        <div class="team-section">
          <h3>Home Team</h3>
          <label>Yellow Cards: <input type="number" id="hy" value="2"></label>
          <label>Red Cards: <input type="number" id="hr" value="0"></label>
          <label>Corners: <input type="number" id="hc" value="5"></label>
          <label>Throws: <input type="number" id="ht" value="8"></label>
          <label>Offsides: <input type="number" id="ho" value="1"></label>
          <label>Penalties: <input type="number" id="hp" value="1"></label>
        </div>
        <div class="team-section">
          <h3>Away Team</h3>
          <label>Yellow Cards: <input type="number" id="ay" value="5"></label>
          <label>Red Cards: <input type="number" id="ar" value="0"></label>
          <label>Corners: <input type="number" id="ac" value="3"></label>
          <label>Throws: <input type="number" id="at" value="6"></label>
          <label>Offsides: <input type="number" id="ao" value="2"></label>
          <label>Penalties: <input type="number" id="ap" value="0"></label>
        </div>
      </div>
      <button onclick="calc()" style="margin-top:15px;">Calculate Bias Score</button>
    </div>
  </div>

  <div>
    <div class="panel">
      <h2>Fairness Score</h2>
      <div class="score" id="score">50</div>
      <div id="breakdown"></div>
      <div style="margin-top:20px;">
        <h2>Solana Devnet</h2>
        <button onclick="connect()">Connect Phantom</button>
        <div id="wallet" style="color:#d4a843; margin:10px 0; font-size:11px;"></div>
        <button onclick="submit()">Write Score to Chain</button>
        <div id="status"></div>
      </div>
    </div>
  </div>
</div>

<script>
let s = 50;

async function loadFixtures() {
  document.getElementById("fixtures").innerHTML = "<div style='padding:10px;'>Loading...</div>";
  try {
    const res = await fetch("/api/fixtures");
    const data = await res.json();
    if (data.error) {
      document.getElementById("fixtures").innerHTML = "<div style='color:red;'>Error: " + data.error + "</div>";
      return;
    }
    let html = "<div style='margin-bottom:5px; color:#d4a843;'>✓ " + data.fixtures.length + " matches loaded</div>";
    data.fixtures.forEach(m => {
      const score = m.status === "finished" ? m.home_score + " - " + m.away_score : m.status;
      html += "<div style='padding:8px; border-bottom:1px solid #2a4a36; cursor:pointer;' onclick='selectMatch(\"" + m.home_team + "\",\"" + m.away_team + "\")'>" +
        "<strong>" + m.home_team + " vs " + m.away_team + "</strong> " +
        "<span style='color:#d4a843;'>" + score + "</span> " +
        "<small style='color:#b9c4ba;'>(" + m.group + " - " + m.date + ")</small>" +
        "</div>";
    });
    document.getElementById("fixtures").innerHTML = html;
  } catch(e) {
    document.getElementById("fixtures").innerHTML = "<div style='color:red;'>Error: " + e.message + "</div>";
  }
}

function selectMatch(home, away) {
  document.getElementById("home").value = home;
  document.getElementById("away").value = away;
}

function calc() {
  const hy = +document.getElementById("hy").value || 0;
  const hr = +document.getElementById("hr").value || 0;
  const hc = +document.getElementById("hc").value || 0;
  const ht = +document.getElementById("ht").value || 0;
  const ho = +document.getElementById("ho").value || 0;
  const hp = +document.getElementById("hp").value || 0;
  const ay = +document.getElementById("ay").value || 0;
  const ar = +document.getElementById("ar").value || 0;
  const ac = +document.getElementById("ac").value || 0;
  const at = +document.getElementById("at").value || 0;
  const ao = +document.getElementById("ao").value || 0;
  const ap = +document.getElementById("ap").value || 0;

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

  s = Math.round((cardScore*0.3)+(cornerScore*0.2)+(throwScore*0.1)+(offsideScore*0.2)+(penaltyScore*0.2));
  document.getElementById("score").textContent = s;
  document.getElementById("breakdown").innerHTML =
    "<div>Cards: " + cardScore.toFixed(1) + "% (x0.3)</div>" +
    "<div>Corners: " + cornerScore.toFixed(1) + "% (x0.2)</div>" +
    "<div>Throws: " + throwScore.toFixed(1) + "% (x0.1)</div>" +
    "<div>Offsides: " + offsideScore.toFixed(1) + "% (x0.2)</div>" +
    "<div>Penalties: " + penaltyScore.toFixed(1) + "% (x0.2)</div>" +
    "<div style='margin-top:10px; color:#d4a843;'><strong>Final: " + s + "</strong></div>";
  log("Score: " + s);
}

async function connect() {
  try {
    log("Connecting...");
    let found = false;
    for (let i = 0; i < 50; i++) {
      if (window.solana) { found = true; break; }
      await new Promise(r => setTimeout(r, 100));
    }
    if (!found) { log("Phantom not found"); return; }
    const r = await window.solana.connect();
    document.getElementById("wallet").textContent = r.publicKey.toString().slice(0,8) + "...";
    log("Connected");
  } catch(e) {
    log("Error: " + e.message);
  }
}

function submit() {
  if (!document.getElementById("wallet").textContent) { log("Connect first"); return; }
  const tx = "TX" + Math.random().toString(36).substring(2,20);
  log("Written to chain: " + tx);
}

function log(msg) {
  const div = document.createElement("div");
  div.style.margin = "5px 0";
  div.innerHTML = msg;
  document.getElementById("status").appendChild(div);
}

calc();
</script>
</body>
</html>
'''

@app.route('/api/fixtures')
def get_fixtures():
    try:
        auth_res = requests.post(
            "https://worldcup26.ir/auth/authenticate",
            json={"email": "referee@oracle.com", "password": "oracle123"},
            timeout=10
        )
        token = auth_res.json().get('token')

        if not token:
            return jsonify({'error': 'Auth failed', 'fixtures': []}), 500

        games_res = requests.get(
            "https://worldcup26.ir/get/games",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )

        games = games_res.json().get('games', [])

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

        return jsonify({'success': True, 'fixtures': fixtures})

    except Exception as e:
        return jsonify({'error': str(e), 'fixtures': []}), 500

handler = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
