"""
API Routes for DreamSpin Casino Games
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.game_history import GameHistory
from app import db
import random
import hashlib
import time

api_bp = Blueprint('api', __name__)

@api_bp.route('/play-coinflip', methods=['POST'])
@login_required
def play_coinflip():
    """Coinflip game API"""
    try:
        data = request.get_json()
        choice = data.get('choice')  # 'heads' or 'tails'
        bet_amount = float(data.get('bet_amount', 0))
        
        # Validate
        if bet_amount <= 0 or bet_amount > current_user.balance:
            return jsonify({'success': False, 'message': 'Invalid bet amount'})
        
        if choice not in ['heads', 'tails']:
            return jsonify({'success': False, 'message': 'Invalid choice'})
        
        # Deduct bet
        current_user.balance -= bet_amount
        
        # Generate result
        result = random.choice(['heads', 'tails'])
        won = result == choice
        payout = bet_amount * 2 if won else 0
        
        # Update balance
        if won:
            current_user.balance += payout
        
        # Save to history
        game_history = GameHistory(
            player_id=current_user.id,
            game_type='coinflip',
            bet_amount=bet_amount,
            result=f"{choice} -> {result}",
            win_amount=payout if won else 0
        )
        db.session.add(game_history)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'result': result,
            'won': won,
            'payout': payout,
            'balance': current_user.balance
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@api_bp.route('/play-dice', methods=['POST'])
@login_required
def play_dice():
    """Dice game API - win zone model (0-100 range)"""
    try:
        from app.utils.provably_fair import ProvablyFair

        data = request.get_json()
        min_val = float(data.get('min_val', 13))
        max_val = float(data.get('max_val', 66))
        bet_amount = float(data.get('bet_amount', 0))

        # Validate bet
        if bet_amount <= 0 or bet_amount > current_user.balance:
            return jsonify({'success': False, 'message': 'Invalid bet amount'})

        # Validate win zone
        if min_val < 1 or max_val > 99 or min_val >= max_val:
            return jsonify({'success': False, 'message': 'Invalid win zone'})

        win_chance = (max_val - min_val) / 100.0
        if win_chance < 0.01 or win_chance > 0.98:
            return jsonify({'success': False, 'message': 'Win chance must be between 1% and 98%'})

        # Generate provably fair roll
        nonce = current_user.nonce
        result = ProvablyFair.generate_result(
            current_user.server_seed, current_user.client_seed, nonce
        )
        roll = round(result * 100, 2)

        # Increment nonce
        current_user.nonce += 1

        # Determine win
        won = min_val <= roll <= max_val
        multiplier = (1 - 0.01) / win_chance
        payout = round(bet_amount * multiplier, 4) if won else 0
        profit = round(payout - bet_amount, 4)

        # Update balance
        current_user.balance = round(current_user.balance - bet_amount + payout, 4)
        current_user.total_wagered = round(current_user.total_wagered + bet_amount, 4)
        current_user.games_played += 1
        if won:
            current_user.total_won = round(current_user.total_won + payout, 4)

        # Save to history
        game_history = GameHistory(
            player_id=current_user.id,
            game_type='dice',
            bet_amount=bet_amount,
            server_seed=current_user.server_seed,
            server_seed_hash=current_user.server_seed_hash,
            client_seed=current_user.client_seed,
            nonce=nonce,
            result_data={
                'roll': roll,
                'min_val': min_val,
                'max_val': max_val,
                'won': won,
                'multiplier': round(multiplier, 4),
            }
        )
        game_history.set_result(payout, profit)
        db.session.add(game_history)
        db.session.commit()

        return jsonify({
            'success': True,
            'roll': roll,
            'won': won,
            'payout': payout,
            'profit': profit,
            'bet_amount': bet_amount,
            'balance': round(current_user.balance, 4),
            'game_id': game_history.id,
            'username': current_user.username,
            'multiplier': round(multiplier, 4),
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

# In-memory store for pending crash rounds (game_key → game data)
_pending_crash = {}

@api_bp.route('/crash-start', methods=['POST'])
@login_required
def crash_start():
    """Start a crash round: deduct bets, return provably-fair crash point."""
    from app.games.crash import CrashGame

    try:
        data = request.get_json()
        bets = data.get('bets', [])  # [{amount, auto_cashout}, ...]

        total_bet = round(sum(float(b.get('amount', 0)) for b in bets), 4)

        if total_bet <= 0:
            return jsonify({'success': False, 'message': 'No bets placed'})
        if total_bet > current_user.balance:
            return jsonify({'success': False, 'message': 'Insufficient balance'})

        nonce = current_user.nonce
        crash_point = CrashGame.generate_crash_point(
            current_user.server_seed, current_user.client_seed, nonce
        )
        current_user.nonce += 1
        current_user.balance = round(current_user.balance - total_bet, 4)
        current_user.total_wagered = round(current_user.total_wagered + total_bet, 4)
        current_user.games_played += 1
        db.session.commit()

        game_key = f"{current_user.id}_{nonce}_{int(time.time() * 1000)}"
        _pending_crash[game_key] = {
            'player_id': current_user.id,
            'crash_point': crash_point,
            'bets': bets,
            'total_bet': total_bet,
            'server_seed': current_user.server_seed,
            'server_seed_hash': current_user.server_seed_hash,
            'client_seed': current_user.client_seed,
            'nonce': nonce,
        }

        return jsonify({
            'success': True,
            'crash_point': crash_point,
            'game_key': game_key,
            'hash': current_user.server_seed_hash,
            'balance': current_user.balance,
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@api_bp.route('/crash-finish', methods=['POST'])
@login_required
def crash_finish():
    """Finish a crash round: validate cashouts, pay out wins, record history."""
    try:
        data = request.get_json()
        game_key = data.get('game_key')
        cashouts = data.get('cashouts', [])  # [{bet_idx, cashout_at}, ...]

        game = _pending_crash.pop(game_key, None)
        if not game or game['player_id'] != current_user.id:
            return jsonify({'success': False, 'message': 'Invalid or expired game'})

        crash_point = game['crash_point']
        bets = game['bets']
        total_payout = 0.0
        results = []

        for cashout in cashouts:
            idx = int(cashout.get('bet_idx', 0))
            cashout_at = float(cashout.get('cashout_at', 0))
            if idx >= len(bets):
                continue
            bet_amount = float(bets[idx].get('amount', 0))
            won = cashout_at >= 1.01 and cashout_at <= crash_point
            payout = round(bet_amount * cashout_at, 4) if won else 0.0
            total_payout += payout
            results.append({'bet_idx': idx, 'won': won, 'payout': payout, 'cashout_at': cashout_at})

        profit = round(total_payout - game['total_bet'], 4)
        current_user.balance = round(current_user.balance + total_payout, 4)
        if total_payout > 0:
            current_user.total_won = round(current_user.total_won + total_payout, 4)

        game_history = GameHistory(
            player_id=current_user.id,
            game_type='crash',
            bet_amount=game['total_bet'],
            server_seed=game['server_seed'],
            server_seed_hash=game['server_seed_hash'],
            client_seed=game['client_seed'],
            nonce=game['nonce'],
            result_data={
                'crash_point': crash_point,
                'bets': bets,
                'cashouts': cashouts,
                'results': results,
            }
        )
        game_history.set_result(total_payout, profit)
        db.session.add(game_history)
        db.session.commit()

        return jsonify({
            'success': True,
            'crash_point': crash_point,
            'results': results,
            'balance': current_user.balance,
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@api_bp.route('/play-roulette', methods=['POST'])
@login_required
def play_roulette():
    """PLG-style roulette: numbers 0-14 (0=green, 1-7=red, 8-14=black)."""
    from app.utils.provably_fair import ProvablyFair
    try:
        data  = request.get_json()
        bets  = data.get('bets', [])   # [{type, value, amount}, ...]

        total_bet = round(sum(float(b.get('amount', 0)) for b in bets), 4)

        if total_bet < 0:
            return jsonify({'success': False, 'message': 'Invalid bet'})
        if total_bet > 0 and total_bet > current_user.balance:
            return jsonify({'success': False, 'message': 'Insufficient balance'})

        # Provably fair result 0-14
        nonce = current_user.nonce
        raw   = ProvablyFair.generate_result(
            current_user.server_seed, current_user.client_seed, nonce)
        result = int(raw * 15)          # 0..14
        result = min(result, 14)
        current_user.nonce += 1

        red_nums  = list(range(1, 8))   # 1-7
        black_nums= list(range(8, 15))  # 8-14
        even_nums = [2, 4, 6, 8, 10, 12, 14]
        odd_nums  = [1, 3, 5,  7,  9, 11, 13]

        total_won   = 0.0
        bet_results = []

        for bet in bets:
            btype  = bet.get('type', '')
            bvalue = str(bet.get('value', ''))
            amount = float(bet.get('amount', 0))
            if amount <= 0:
                continue

            won  = False
            mult = 0

            if btype == 'color':
                if   bvalue == 'red'   and result in red_nums:   won = True; mult = 2
                elif bvalue == 'black' and result in black_nums: won = True; mult = 2
                elif bvalue == 'even'  and result in even_nums:  won = True; mult = 2
                elif bvalue == 'odd'   and result in odd_nums:   won = True; mult = 2
            elif btype == 'number':
                if result == int(bvalue):
                    won = True; mult = 14   # zero pays 14x

            payout     = round(amount * mult, 4) if won else 0.0
            total_won += payout
            bet_results.append({
                'type': btype, 'value': bvalue,
                'amount': amount, 'won': won, 'payout': payout
            })

        if total_bet > 0:
            profit = round(total_won - total_bet, 4)
            current_user.balance      = round(current_user.balance - total_bet + total_won, 4)
            current_user.total_wagered= round(current_user.total_wagered + total_bet, 4)
            current_user.games_played += 1
            if total_won > 0:
                current_user.total_won = round(current_user.total_won + total_won, 4)

            gh = GameHistory(
                player_id=current_user.id,
                game_type='roulette',
                bet_amount=total_bet,
                server_seed=current_user.server_seed,
                server_seed_hash=current_user.server_seed_hash,
                client_seed=current_user.client_seed,
                nonce=nonce,
                result_data={'result': result, 'bets': bets, 'bet_results': bet_results}
            )
            gh.set_result(total_won, profit)
            db.session.add(gh)

        db.session.commit()

        return jsonify({
            'success': True,
            'result': result,
            'total_won': round(total_won, 4),
            'total_bet': round(total_bet, 4),
            'bet_results': bet_results,
            'balance': current_user.balance,
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})
