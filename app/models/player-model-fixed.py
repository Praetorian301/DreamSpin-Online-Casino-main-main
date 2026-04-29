# app/models/player.py
from app import db
from datetime import datetime

class Player(db.Model):
    __tablename__ = 'players'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    balance = db.Column(db.Float, default=1000.0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    game_history = db.relationship('GameHistory', backref='player', lazy=True)
    
    def __init__(self, username, balance=1000.0):
        """Initialize player with username and optional balance"""
        self.username = username
        self.balance = balance
    
    def __repr__(self):
        return f'<Player {self.username}>'
    
    def update_balance(self, amount):
        """Update player balance"""
        self.balance += amount
        db.session.commit()
    
    def deduct_balance(self, amount):
        """Deduct from player balance"""
        if self.balance >= amount:
            self.balance -= amount
            db.session.commit()
            return True
        return False
    
    def add_balance(self, amount):
        """Add to player balance"""
        self.balance += amount
        db.session.commit()
