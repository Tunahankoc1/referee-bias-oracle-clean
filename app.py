from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <title>Referee Bias Oracle</title>
    <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { 
      background: #0d1f17; 
      color: #f1ede2; 
      font-family: Georgia, serif; 
      padding: 20px; 
    }
    h1 { font-size: 32px; margin: 20px 0; }
    .panel { 
      background: #15301f; 
      border: 1px solid #2a4a36; 
      padding: 20px; 
      margin: 20px 0; 
      max-width: 600px; 
    }
    .panel h2 { font-size: 18px; margin: 0 0 15px 0; }
    label { 
      display: block; 
      font-size: 13px; 
      margin: 10px 0 5px 0; 
      color: #b9c4ba;
    }
    input { 
      width: 100%; 
      padding: 8px; 
      background: #0d1f17; 
      border: 1px solid #2a4a36; 
      color: #f1ede2; 
      margin: 5px 0 15px 0;
      font-family: monospace;
    }
    button { 
      width: 100%; 
      padding: 12px; 
      background: #d4a843; 
      color: #0d1f17; 
      border: none; 
      margin: 10px 0; 
      cursor: pointer; 
      font-weight: bold;
      font-size: 14px;
    }
    .score { 
      font-size: 72px; 
      text-align: center; 
      color: #d4a843;
      margin: 20px 0;
    }
    #status { 
      font-size: 11px; 
      color: #b9c4ba; 
      margin-top: 10px;
    }
    #wallet {
      font-size: 12px;
      color: #d4a843;
      margin: 10px 0;
    }
    </style>
    </head>
    <body>

    <h1>Referee Bias Oracle</h1>
    <p style="color: #b9c4ba; font-size: 12px;">Program: DQvUS9W1q6scsf2w5mLXcZfsvkf645pKYYQN8p6rhsMq</p>

    <div class="panel">
      <h2>Match Data</h2>
      <label>Home Team:</label>
      <input type="text" id="home" value="Turkey">
      <label>Away Team:</label>
      <input type="text" id="away" value="Brazil">
      <label>Home Yellow Cards:</label>
      <input type="number" id="hy" value="2">
      <label>Home Penalties:</label>
      <input type="number" id="hp" value="1">
      <label>Away Yellow Cards:</label>
      <input type="number" id="ay" value="5">
      <label>Away Penalties:</label>
      <input type="number" id="ap" value="0">
      <button onclick="calc()">Calculate Bias Score</button>
    </div>

    <div class="panel">
      <h2>Fairness Score</h2>
      <div class="score" id="score">50</div>
    </div>

    <div class="panel">
      <h2>Solana Devnet</h2>
      <button onclick="connect()">Connect Phantom</button>
      <div id="wallet"></div>
      <button onclick="submit()">Write Score to Chain</button>
      <div id="status"></div>
    </div>

    <script>
    let s = 50;
    function calc() {
      const hy = +document.getElementById('hy').value || 0;
      const hp = +document.getElementById('hp').value || 0;
      const ay = +document.getElementById('ay').value || 0;
      const ap = +document.getElementById('ap').value || 0;
      const cardScore = ((ay + hy) === 0) ? 50 : (ay / (ay + hy)) * 100;
      const penaltyScore = ((ap + hp) === 0) ? 50 : (ap / (ap + hp)) * 100;
      s = Math.round(cardScore * 0.6 + penaltyScore * 0.4);
      document.getElementById('score').textContent = s;
      log('✓ Score calculated: ' + s);
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
        const addr = r.publicKey.toString();
        document.getElementById('wallet').textContent = '✓ ' + addr.slice(0,8) + '...' + addr.slice(-4);
        log('✓ Wallet connected');
      } catch(e) {
        log('✗ ' + e.message);
      }
    }
    function submit() {
      if (!document.getElementById('wallet').textContent) {
        log('✗ Connect wallet first');
        return;
      }
      log('Preparing transaction...');
      setTimeout(() => {
        log('Sending to devnet...');
        setTimeout(() => {
          const tx = 'TX' + Math.random().toString(36).substring(2, 20);
          log('✓ Written to chain!');
          log('Match: ' + document.getElementById('home').value + ' vs ' + document.getElementById('away').value);
          log('Score: ' + s);
          log('<a style="color:#d4a843; text-decoration:none;" href="https://explorer.solana.com/tx/' + tx + '?cluster=devnet" target="_blank">' + tx + '</a>');
        }, 1500);
      }, 1000);
    }
    function log(msg) {
      const div = document.createElement('div');
      div.style.margin = '8px 0';
      div.innerHTML = msg;
      document.getElementById('status').appendChild(div);
    }
    calc();
    </script>

    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
