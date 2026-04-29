"""
Main routes for DreamSpin Casino
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.player import Player
from app.models.game_history import GameHistory
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page - show games if logged in, login form if not"""
    if current_user.is_authenticated:
        return render_template('index.html', player=current_user)
    return redirect(url_for('main.login'))

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        
        if not username:
            flash('Please enter a username', 'error')
            return render_template('login.html')
        
        # Find or create player
        player = Player.query.filter_by(username=username).first()
        
        if not player:
            # Create new player with starting balance
            player = Player(username=username)
            db.session.add(player)
            db.session.commit()
            flash(f'Welcome to DreamSpin, {username}! You have $1000 to play with.', 'success')
        else:
            flash(f'Welcome back, {username}!', 'success')
        
        login_user(player)
        return redirect(url_for('main.index'))
    
    return render_template('login.html')

@main_bp.route('/logout')
@login_required
def logout():
    """Logout current user"""
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('main.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page with player stats"""
    # Calculate stats from game history
    history = GameHistory.query.filter_by(player_id=current_user.id).all()
    
    stats = {
        'total_bets': len(history),
        'total_wagered': sum(h.bet_amount for h in history),
        'total_won': sum(h.payout for h in history)
    }
    
    return render_template('dashboard.html', player=current_user, stats=stats)

@main_bp.route('/profile')
@login_required
def profile():
    """Player profile page"""
    return render_template('profile.html', player=current_user)

@main_bp.route('/history')
@login_required
def history():
    """Game history page"""
    # Get all game history for current player
    history = GameHistory.query.filter_by(player_id=current_user.id)\
        .order_by(GameHistory.timestamp.desc())\
        .limit(100)\
        .all()
    
    return render_template('history.html', player=current_user, history=history)

@main_bp.route('/reset-balance', methods=['POST'])
@login_required
def reset_balance():
    """Reset player balance to $1000"""
    current_user.balance = 1000.0
    db.session.commit()
    flash('Your balance has been reset to $1000!', 'success')
    return redirect(url_for('main.dashboard'))

# Deposit/Withdraw Routes
@main_bp.route('/deposit/crypto')
@login_required
def crypto_deposit():
    """Crypto deposit page"""
    return render_template('crypto_deposit.html', player=current_user)

@main_bp.route('/withdraw/crypto')
@login_required
def crypto_withdraw():
    """Crypto withdraw page"""
    return render_template('crypto_withdraw.html', player=current_user)

# Provably Fair Routes
@main_bp.route('/provably-fair/<game_type>')
@login_required
def provably_fair(game_type):
    """Provably fair verification page"""
    return render_template('provably_fair.html', player=current_user, game_type=game_type)

# Bonuses Route
@main_bp.route('/bonuses')
@login_required
def bonuses():
    """Bonuses and promotions page"""
    return render_template('bonuses.html', player=current_user)

# Legal Pages Routes
@main_bp.route('/about-us')
def about_us():
    """About Us page"""
    return render_template('legal/about_us.html')

@main_bp.route('/tos')
def tos():
    """Terms of Service page"""
    return render_template('legal/tos.html')

@main_bp.route('/responsible-gaming')
def responsible_gaming():
    """Responsible Gaming page"""
    return render_template('legal/responsible_gaming.html')

@main_bp.route('/kyc')
def kyc():
    """KYC Verification page"""
    return render_template('legal/kyc.html')

@main_bp.route('/privacy-policy')
def privacy_policy():
    """Privacy Policy page"""
    return render_template('legal/privacy_policy.html')

@main_bp.route('/cookie-policy')
def cookie_policy():
    """Cookie Policy page"""
    return render_template('legal/cookie_policy.html')
