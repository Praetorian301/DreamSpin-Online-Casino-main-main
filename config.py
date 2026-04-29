import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///dreamspin.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Game Settings
    STARTING_BALANCE = 1000.00
    MAX_BET = 100.00
    MIN_BET = 0.10
    
    # House Edge (%)
    DICE_HOUSE_EDGE = 1.0
    ROULETTE_HOUSE_EDGE = 2.7  # European roulette standard
    COINFLIP_HOUSE_EDGE = 2.0
    CRASH_HOUSE_EDGE = 1.0
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
