"""
Game History Model - Tracks all game results for verification
"""
from datetime import datetime
from app import db

class GameHistory(db.Model):
    """Game history model for provably fair verification"""
    __tablename__ = 'game_history'
    
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    
    # Game Info
    game_type = db.Column(db.String(20), nullable=False)  # dice, roulette, coinflip, crash
    bet_amount = db.Column(db.Float, nullable=False)
    payout = db.Column(db.Float, default=0.0)
    profit = db.Column(db.Float, default=0.0)
    
    # Provably Fair Data
    server_seed = db.Column(db.String(128), nullable=False)
    server_seed_hash = db.Column(db.String(64), nullable=False)
    client_seed = db.Column(db.String(128), nullable=False)
    nonce = db.Column(db.Integer, nullable=False)
    
    # Game-Specific Results
    result_data = db.Column(db.JSON)  # Stores game-specific data
    
    # Timestamps
    played_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, player_id, game_type, bet_amount, server_seed, 
                 server_seed_hash, client_seed, nonce, result_data):
        self.player_id = player_id
        self.game_type = game_type
        self.bet_amount = bet_amount
        self.server_seed = server_seed
        self.server_seed_hash = server_seed_hash
        self.client_seed = client_seed
        self.nonce = nonce
        self.result_data = result_data
    
    def set_result(self, payout, profit):
        """Set the game result"""
        self.payout = payout
        self.profit = profit
    
    def to_dict(self):
        """Convert to dictionary for JSON response"""
        return {
            'id': self.id,
            'game_type': self.game_type,
            'bet_amount': self.bet_amount,
            'payout': self.payout,
            'profit': self.profit,
            'server_seed_hash': self.server_seed_hash,
            'client_seed': self.client_seed,
            'nonce': self.nonce,
            'result_data': self.result_data,
            'played_at': self.played_at.isoformat()
        }
    
    def __repr__(self):
        return f'<GameHistory {self.game_type} - ${self.bet_amount}>'
