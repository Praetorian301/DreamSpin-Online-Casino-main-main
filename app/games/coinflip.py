"""
Coinflip Game Engine

Simple 50/50 game - bet on heads or tails
Payout: ~1.96x (with 2% house edge)
"""
from app.utils.provably_fair import ProvablyFair

class CoinflipGame:
    """Coinflip game logic"""
    
    HOUSE_EDGE = 0.02  # 2% house edge
    MULTIPLIER = 2.0
    
    @staticmethod
    def play(server_seed: str, client_seed: str, nonce: int, player_choice: str, bet_amount: float):
        """
        Play a coinflip game
        
        Args:
            server_seed: Server's secret seed
            client_seed: Client's seed
            nonce: Current nonce
            player_choice: 'heads' or 'tails'
            bet_amount: Amount wagered
            
        Returns:
            Dictionary with game result
        """
        # Validate choice
        if player_choice not in ['heads', 'tails']:
            raise ValueError("Choice must be 'heads' or 'tails'")
        
        # Generate fair result
        result = ProvablyFair.generate_result(server_seed, client_seed, nonce)
        flip_result = ProvablyFair.result_to_coinflip(result)
        
        # Check win condition
        is_win = flip_result == player_choice
        
        # Calculate payout with house edge
        multiplier = CoinflipGame.MULTIPLIER * (1 - CoinflipGame.HOUSE_EDGE)
        payout = bet_amount * multiplier if is_win else 0
        profit = payout - bet_amount
        
        return {
            'result': flip_result,
            'player_choice': player_choice,
            'is_win': is_win,
            'multiplier': multiplier,
            'bet_amount': bet_amount,
            'payout': payout,
            'profit': profit,
            'raw_result': result
        }
    
    @staticmethod
    def get_game_info():
        """Get game information for UI"""
        return {
            'name': 'Coinflip',
            'house_edge': CoinflipGame.HOUSE_EDGE * 100,
            'multiplier': CoinflipGame.MULTIPLIER * (1 - CoinflipGame.HOUSE_EDGE),
            'description': 'Heads or tails? 50/50 chance to double your bet!'
        }
