# 🎰 DreamSpin - Digital Casino

A play-money casino simulator with provably fair gaming mechanics

## 🎮 Games Included
- 🎲 Dice
- 🎡 Roulette
- 🪙 Coinflip
- 🚀 Crash

## 🚀 Quick Start

### Installation
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Application
```bash
# Development mode
python run.py

# Or with Flask directly
flask run
```

Open browser to: `http://localhost:5000`

## 📁 Project Layout
```
📂 DreamSpin-Online-Casino/
│
├── 📂 app/
│   ├── 📂 games/
│   │   ├── dice.py
│   │   ├── roulette.py
│   │   ├── coinflip.py
│   │   ├── crash.py
│   │   └── __init__.py
│   │
│   ├── 📂 models/
│   │   ├── player.py
│   │   ├── game_history.py
│   │   ├── player-model-fixed.py
│   │   └── __init__.py
│   │
│   ├── 📂 routes/
│   │   ├── main.py
│   │   ├── games.py
│   │   ├── api.py
│   │   ├── login-route-fixed.py
│   │   └── __init__.py
│   │
│   ├── 📂 utils/
│   │   ├── provably_fair.py
│   │   └── __init__.py
│   │
│   ├── 📂 static/
│   │   ├── 📂 css/
│   │   │   ├── style.css
│   │   │   └── roulette-plg.css
│   │   │
│   │   ├── 📂 js/
│   │   │   └── main.js
│   │   │
│   │   └── 📂 favicon/
│   │       ├── favicon80.png
│   │       └── favicon90.png
│   │
│   ├── 📂 templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── bonuses.html
│   │   ├── crypto_deposit.html
│   │   ├── crypto_withdraw.html
│   │   ├── provably_fair.html
│   │   │
│   │   ├── 📂 games/
│   │   │   ├── dice.html
│   │   │   ├── roulette.html
│   │   │   ├── coinflip.html
│   │   │   └── crash.html
│   │   │
│   │   └── 📂 legal/
│   │       ├── about_us.html
│   │       ├── tos.html
│   │       ├── privacy_policy.html
│   │       ├── cookie_policy.html
│   │       ├── kyc.html
│   │       └── responsible_gaming.html
│   │
│   └── __init__.py
│
├── 📂 instance/
│   └── dreamspin.db
│
├── config.py
├── run.py
├── requirements.txt
└── README.md
```

## 🔐 Provably Fair System
All games use cryptographic verification:
- Server Seed (hashed)
- Client Seed (player provided)
- Nonce (incremental)
- HMAC-SHA256 for result generation

## 💰 Play Money Only
- No real money involved
- Free starting balance: $1000
- Safe learning environment

## 📝 License
Educational purposes only.
