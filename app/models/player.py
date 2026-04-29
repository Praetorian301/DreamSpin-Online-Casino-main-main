"""
Player Model - Manages player accounts and balances
"""
from datetime import datetime
from flask_login import UserMixin
from app import db
import secrets

class Player(UserMixin, db.Model):
    """Player account model"""
    __tablename__ = 'players'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    balance = db.Column(db.Float, default=1000.00)
    total_wagered = db.Column(db.Float, default=0.0)
    total_won = db.Column(db.Float, default=0.0)
    games_played = db.Column(db.Integer, default=0)
    
    # Provably Fair Seeds
    server_seed = db.Column(db.String(128), nullable=False)
    server_seed_hash = db.Column(db.String(64), nullable=False)
    client_seed = db.Column(db.String(128), nullable=False)
    nonce = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    game_history = db.relationship('GameHistory', backref='player', lazy=True)
    
    def __init__(self, username):
        self.username = username
        self.balance = 1000.00
        self.server_seed = secrets.token_hex(32)
        self.client_seed = secrets.token_hex(16)
        self._generate_server_seed_hash()
    
    def _generate_server_seed_hash(self):
        """Generate SHA-256 hash of server seed"""
        import hashlib
        self.server_seed_hash = hashlib.sha256(self.server_seed.encode()).hexdigest()
    
    def rotate_seeds(self):
        """Rotate to new seeds (called when player requests)"""
        old_server_seed = self.server_seed
        self.server_seed = secrets.token_hex(32)
        self.nonce = 0
        self._generate_server_seed_hash()
        return old_server_seed
    
    def update_balance(self, amount):
        """Update player balance"""
        self.balance += amount
        db.session.commit()
    
    def place_bet(self, amount):
        """Deduct bet from balance"""
        if amount > self.balance:
            return False
        self.balance -= amount
        self.total_wagered += amount
        self.games_played += 1
        self.nonce += 1
        db.session.commit()
        return True
    
    def add_winnings(self, amount):
        """Add winnings to balance"""
        self.balance += amount
        self.total_won += amount
        db.session.commit()
    
    def __repr__(self):
        return f'<Player {self.username}>'
