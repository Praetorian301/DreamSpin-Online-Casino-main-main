# app/routes/main.py - LOGIN ROUTE FIX

from ast import main
from flask import flash, redirect, render_template, request, session, url_for
from app.models.player import Player


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        
        if not username:
            flash('Username is required', 'error')
            return redirect(url_for('main.login'))
        
        # Check if player exists
        player = Player.query.filter_by(username=username).first()
        
        if not player:
            # Create new player with balance parameter
            try:
                player = Player(username=username, balance=1000.0)
                db.session.add(player)
                db.session.commit()
                flash(f'Welcome {username}! You have been given $1000 to start.', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error creating player: {str(e)}', 'error')
                return redirect(url_for('main.login'))
        else:
            flash(f'Welcome back {username}!', 'success')
        
        # Set session
        session['player_id'] = player.id
        session['username'] = player.username
        
        return redirect(url_for('main.dashboard'))
    
    return render_template('login.html')
