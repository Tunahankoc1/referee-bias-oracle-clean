# Referee Bias Oracle

On-chain referee bias analysis for World Cup 2026 matches — powered by live match data and recorded permanently on Solana.

🌐 **Live Demo:** [referee-bias-oracle-clean.vercel.app](https://referee-bias-oracle-clean.vercel.app)

---

## What It Does

### 1. Fetches Live Data
- **TxLINE API** — World Cup 2026 fixtures list
- **WorldCup26 API** — live match results and scores

### 2. Generates Match Statistics
Click any match to see realistic referee statistics:
- Yellow cards, red cards
- Corners, offsides, fouls
- Penalties awarded

Statistics are weighted based on match outcome — winners receive statistically favorable metrics, losers unfavorable ones.

### 3. Calculates Bias Score
6-metric weighted algorithm produces a **0–100 bias score**:

| Score | Verdict |
|-------|---------|
| 65+ | 🔴 HOME TEAM FAVORED |
| 35–65 | 🟢 FAIR MATCH |
| 35- | 🔵 AWAY TEAM FAVORED |

### 4. Records On-Chain
- Connect **Phantom** wallet
- Click **"Write Score to Chain"** → real Solana transaction
- Bias score permanently stored on blockchain
- Verifiable on Solana Explorer

---

## Tech Stack

- **Frontend:** HTML + JavaScript (single file, no build step)
- **Blockchain:** Solana (Phantom wallet + Memo program)
- **APIs:** TxLINE (fixtures), WorldCup26 (results)
- **Deployment:** Vercel

---

## How to Run

```bash
# Clone the repo
git clone https://github.com/Tunahankoc1/referee-bias-oracle-clean
cd referee-bias-oracle-clean

# Open in browser
open index.html
# or visit the live demo
```

**Requirements:**
- Phantom wallet browser extension
- Small amount of SOL for transaction fees

---

## Built For

[Superteam World Cup Hackathon](https://superteam.fun/earn/hackathon/world-cup) — Markets Track
