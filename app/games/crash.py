"""
Crash Game Engine

The multiplier starts at 1.00x and increases until it "crashes"
Players must cash out before the crash to win
The crash point is determined by provably fair system

Example:
- Crash at 2.45x: Players who cashed out before 2.45x win
- If you bet $10 and cash out at 2.00x, you win $20
"""
from app.utils.provably_fair import ProvablyFair

class CrashGame:
    """Crash game logic"""
    
    HOUSE_EDGE = 0.01  # 1% house edge
    MIN_CASHOUT = 1.01  # Minimum cashout multiplier
    
    @staticmethod
    def generate_crash_point(server_seed: str, client_seed: str, nonce: int) -> float:
        """
        Generate the crash point for a game
        
        Args:
            server_seed: Server's secret seed
            client_seed: Client's seed
            nonce: Current nonce
            
        Returns:
            Crash multiplier (e.g., 2.45x)
        """
        result = ProvablyFair.generate_result(server_seed, client_seed, nonce)
        crash_point = ProvablyFair.result_to_crash(result, CrashGame.HOUSE_EDGE)
        return crash_point
    
    @staticmethod
    def play(server_seed: str, client_seed: str, nonce: int, bet_amount: float, cashout_at: float = None):
        """
        Play a crash game
        
        Args:
            server_seed: Server's secret seed
            client_seed: Client's seed
            nonce: Current nonce
            bet_amount: Amount wagered
            cashout_at: Multiplier to auto cash out at (optional)
            
        Returns:
            Dictionary with game result
        """
        # Generate crash point
        crash_point = CrashGame.generate_crash_point(server_seed, client_seed, nonce)
        
        # Determine if player won
        if cashout_at is None:
            # No cashout set - player must manually cash out
            is_win = False
            actual_cashout = None
            payout = 0
        elif cashout_at < CrashGame.MIN_CASHOUT:
            raise ValueError(f"Cashout must be at least {CrashGame.MIN_CASHOUT}x")
        elif cashout_at <= crash_point:
            # Player cashed out before crash
            is_win = True
            actual_cashout = cashout_at
            payout = bet_amount * cashout_at
        else:
            # Player's cashout was after crash
            is_win = False
            actual_cashout = cashout_at
            payout = 0
        
        profit = payout - bet_amount if payout > 0 else -bet_amount
        
        return {
            'crash_point': crash_point,
            'cashout_at': cashout_at,
            'actual_cashout': actual_cashout,
            'is_win': is_win,
            'bet_amount': bet_amount,
            'payout': payout,
            'profit': profit
        }
    
    @staticmethod
    def simulate_crash(crash_point: float, step: float = 0.01):
        """
        Simulate crash multiplier progression
        
        Args:
            crash_point: Point where game crashes
            step: Increment step (default 0.01 = 1 cent)
            
        Returns:
            List of multipliers from 1.00 to crash_point
        """
        multipliers = []
        current = 1.00
        
        while current <= crash_point:
            multipliers.append(round(current, 2))
            current += step
        
        return multipliers
    
    @staticmethod
    def get_game_info():
        """Get game information for UI"""
        return {
            'name': 'Crash',
            'house_edge': CrashGame.HOUSE_EDGE * 100,
            'min_cashout': CrashGame.MIN_CASHOUT,
            'description': 'Watch the multiplier climb and cash out before it crashes!'
        }
