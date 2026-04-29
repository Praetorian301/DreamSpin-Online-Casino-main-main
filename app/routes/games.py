"""
Game Routes - All casino games
"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user

games_bp = Blueprint('games', __name__)

@games_bp.route('/dice')
@login_required
def dice():
    """Dice game page"""
    return render_template('games/dice.html', player=current_user)

@games_bp.route('/roulette')
@login_required
def roulette():
    """Roulette game page"""
    return render_template('games/roulette.html', player=current_user)

@games_bp.route('/coinflip')
@login_required
def coinflip():
    """Coin flip game page"""
    return render_template('games/coinflip.html', player=current_user)

@games_bp.route('/crash')
@login_required
def crash():
    """Crash game page"""
    return render_template('games/crash.html', player=current_user)
