"""
Provably Fair System - Cryptographic Game Result Generator

This is the CORE of the entire casino system.
Every game uses this to generate verifiable, fair results.
"""
import hmac
import hashlib

class ProvablyFair:
    """
    Provably Fair RNG System
    
    Uses HMAC-SHA256 to generate verifiable random numbers.
    Formula: HMAC-SHA256(server_seed, client_seed:nonce)
    """
    
    @staticmethod
    def generate_result(server_seed: str, client_seed: str, nonce: int) -> float:
        """
        Generate a fair random number between 0.0 and 1.0
        
        Args:
            server_seed: Secret server seed (revealed after game)
            client_seed: Player-provided seed
            nonce: Incrementing number for each bet
            
        Returns:
            Float between 0.0 and 0.9999999...
        """
        # Create message: "client_seed:nonce"
        message = f"{client_seed}:{nonce}"
        
        # Generate HMAC-SHA256
        hmac_result = hmac.new(
            server_seed.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # Convert first 8 characters of hex to decimal
        # This gives us a number between 0 and 4,294,967,295
        hex_chunk = hmac_result[:8]
        decimal_value = int(hex_chunk, 16)
        
        # Normalize to 0.0 - 1.0
        max_value = 0xFFFFFFFF  # 4,294,967,295
        result = decimal_value / max_value
        
        return result
    
    @staticmethod
    def generate_hash(server_seed: str) -> str:
        """
        Generate SHA-256 hash of server seed (shown to player before game)
        
        Args:
            server_seed: The server seed to hash
            
        Returns:
            64-character hex hash
        """
        return hashlib.sha256(server_seed.encode('utf-8')).hexdigest()
    
    @staticmethod
    def verify_result(server_seed: str, client_seed: str, nonce: int, claimed_result: float) -> bool:
        """
        Verify that a result was generated fairly
        
        Args:
            server_seed: Revealed server seed
            client_seed: Client seed used
            nonce: Nonce used
            claimed_result: The result to verify
            
        Returns:
            True if result is valid, False otherwise
        """
        actual_result = ProvablyFair.generate_result(server_seed, client_seed, nonce)
        return abs(actual_result - claimed_result) < 0.000001  # Allow tiny floating point error
    
    @staticmethod
    def result_to_dice(result: float) -> float:
        """
        Convert 0.0-1.0 result to dice roll (0.00 - 99.99)
        
        Args:
            result: Float from generate_result()
            
        Returns:
            Dice roll value
        """
        return round(result * 100, 2)
    
    @staticmethod
    def result_to_roulette(result: float, max_number: int = 36) -> int:
        """
        Convert 0.0-1.0 result to roulette number
        
        Args:
            result: Float from generate_result()
            max_number: Maximum roulette number (36 for European, 14 for simplified)
            
        Returns:
            Roulette number (0 to max_number)
        """
        return int(result * (max_number + 1))
    
    @staticmethod
    def result_to_coinflip(result: float) -> str:
        """
        Convert 0.0-1.0 result to coin flip
        
        Args:
            result: Float from generate_result()
            
        Returns:
            'heads' or 'tails'
        """
        return 'heads' if result < 0.5 else 'tails'
    
    @staticmethod
    def result_to_crash(result: float, house_edge: float = 0.01) -> float:
        """
        Convert 0.0-1.0 result to crash multiplier
        
        Uses formula: (99 / (1 - result)) / 100
        With house edge adjustment
        
        Args:
            result: Float from generate_result()
            house_edge: House edge (0.01 = 1%)
            
        Returns:
            Crash multiplier (e.g., 2.45x)
        """
        # Prevent division by zero
        if result >= 0.99:
            result = 0.9899
        
        # Calculate crash point with house edge
        crash_point = (99 / (result * 100)) * (1 - house_edge)
        
        # Round to 2 decimal places
        return round(crash_point, 2)
