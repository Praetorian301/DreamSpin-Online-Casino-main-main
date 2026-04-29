"""
Dice Game Engine

Players choose a number (0.00 to 99.99) and bet whether the roll will be UNDER that number.
Higher target = lower multiplier, safer bet
Lower target = higher multiplier, riskier bet

Example:
- Roll under 50.00 = 50% chance = 1.98x multiplier
- Roll under 10.00 = 10% chance = 9.90x multiplier
"""
from app.utils.provably_fair import ProvablyFair

class DiceGame:
    """Dice game logic"""
    
    HOUSE_EDGE = 0.01  # 1% house edge
    MIN_CHANCE = 1.00  # Minimum win chance (%)
    MAX_CHANCE = 98.00  # Maximum win chance (%)
    
    @staticmethod
    def calculate_multiplier(target: float) -> float:
        """
        Calculate payout multiplier based on target number
        
        Args:
            target: Roll under this number (0.00 - 99.99)
            
        Returns:
            Payout multiplier
        """
        win_chance = target / 100.0
        multiplier = (1 - DiceGame.HOUSE_EDGE) / win_chance
        return round(multiplier, 4)
    
    @staticmethod
    def play(server_seed: str, client_seed: str, nonce: int, target: float, bet_amount: float):
        """
        Play a dice game
        
        Args:
            server_seed: Server's secret seed
            client_seed: Client's seed
            nonce: Current nonce
            target: Roll under this number to win
            bet_amount: Amount wagered
            
        Returns:
            Dictionary with game result
        """
        # Validate target
        if target < DiceGame.MIN_CHANCE or target > DiceGame.MAX_CHANCE:
            raise ValueError(f"Target must be between {DiceGame.MIN_CHANCE} and {DiceGame.MAX_CHANCE}")
        
        # Generate fair result
        result = ProvablyFair.generate_result(server_seed, client_seed, nonce)
        roll = ProvablyFair.result_to_dice(result)
        
        # Check win condition
        is_win = roll < target
        
        # Calculate payout
        multiplier = DiceGame.calculate_multiplier(target)
        payout = bet_amount * multiplier if is_win else 0
        profit = payout - bet_amount
        
        return {
            'roll': roll,
            'target': target,
            'is_win': is_win,
            'multiplier': multiplier,
            'bet_amount': bet_amount,
            'payout': payout,
            'profit': profit,
            'win_chance': target,
            'raw_result': result
        }
    
    @staticmethod
    def get_game_info():
        """Get game information for UI"""
        return {
            'name': 'Dice',
            'house_edge': DiceGame.HOUSE_EDGE * 100,
            'min_chance': DiceGame.MIN_CHANCE,
            'max_chance': DiceGame.MAX_CHANCE,
            'description': 'Roll the dice and win if your roll is under the target number!'
        }
