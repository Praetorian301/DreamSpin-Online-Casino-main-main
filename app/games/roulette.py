"""
Roulette Game Engine

European-style roulette with numbers 0-36
- Red numbers: 1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36
- Black numbers: 2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35
- Green: 0

Bet types:
- Red/Black: 2x payout
- Even/Odd: 2x payout
- Single Number: 36x payout
- Zero: 36x payout
"""
from app.utils.provably_fair import ProvablyFair

class RouletteGame:
    """Roulette game logic"""
    
    HOUSE_EDGE = 0.027  # 2.7% house edge (European roulette)
    MAX_NUMBER = 36
    
    # Red numbers in roulette
    RED_NUMBERS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
    
    # Black numbers in roulette
    BLACK_NUMBERS = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
    
    @staticmethod
    def get_color(number: int) -> str:
        """Get color of a roulette number"""
        if number == 0:
            return 'green'
        elif number in RouletteGame.RED_NUMBERS:
            return 'red'
        else:
            return 'black'
    
    @staticmethod
    def play(server_seed: str, client_seed: str, nonce: int, bet_type: str, bet_value, bet_amount: float):
        """
        Play a roulette game
        
        Args:
            server_seed: Server's secret seed
            client_seed: Client's seed
            nonce: Current nonce
            bet_type: Type of bet ('red', 'black', 'even', 'odd', 'number', 'zero')
            bet_value: Value for the bet (number for 'number' bet type)
            bet_amount: Amount wagered
            
        Returns:
            Dictionary with game result
        """
        # Generate fair result
        result = ProvablyFair.generate_result(server_seed, client_seed, nonce)
        number = ProvablyFair.result_to_roulette(result, RouletteGame.MAX_NUMBER)
        color = RouletteGame.get_color(number)
        
        # Determine if bet won
        is_win = False
        multiplier = 0
        
        if bet_type == 'red':
            is_win = color == 'red'
            multiplier = 2.0
        elif bet_type == 'black':
            is_win = color == 'black'
            multiplier = 2.0
        elif bet_type == 'even':
            is_win = number % 2 == 0 and number != 0
            multiplier = 2.0
        elif bet_type == 'odd':
            is_win = number % 2 == 1
            multiplier = 2.0
        elif bet_type == 'zero':
            is_win = number == 0
            multiplier = 36.0
        elif bet_type == 'number':
            is_win = number == bet_value
            multiplier = 36.0
        
        # Calculate payout with house edge
        if is_win:
            payout = bet_amount * multiplier * (1 - RouletteGame.HOUSE_EDGE)
        else:
            payout = 0
        
        profit = payout - bet_amount
        
        return {
            'number': number,
            'color': color,
            'bet_type': bet_type,
            'bet_value': bet_value,
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
            'name': 'Roulette',
            'house_edge': RouletteGame.HOUSE_EDGE * 100,
            'max_number': RouletteGame.MAX_NUMBER,
            'red_numbers': list(RouletteGame.RED_NUMBERS),
            'black_numbers': list(RouletteGame.BLACK_NUMBERS),
            'description': 'Spin the wheel and bet on red, black, or specific numbers!'
        }
