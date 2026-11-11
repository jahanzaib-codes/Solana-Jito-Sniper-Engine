"""
Solana-Jito-Sniper-Engine: Pump.fun Bonding Curve Decoder
Decodes bonding curve creation, virtual reserves, and token graduation events.
"""

from typing import Optional, Dict, Any
from src.models.events import PoolCreationEvent, DexProtocol


class PumpFunDecoder:
    """Decodes Pump.fun bonding curve program telemetry."""

    PUMPFUN_PROGRAM_ID = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"

    @classmethod
    def is_pumpfun_create(cls, log_messages: list) -> bool:
        """Checks if transaction initializes a new Pump.fun bonding curve."""
        for log in log_messages:
            if "Instruction: Create" in log:
                return True
        return False

    @classmethod
    def calculate_bonding_curve_price(cls, virtual_sol_reserves: int, virtual_token_reserves: int) -> float:
        """Computes instantaneous token price in SOL."""
        if virtual_token_reserves == 0:
            return 0.0
        return (virtual_sol_reserves / 1e9) / (virtual_token_reserves / 1e6)

    @classmethod
    def parse_create_event(cls, tx_data: Dict[str, Any]) -> Optional[PoolCreationEvent]:
        """Extracts token mint and bonding curve account."""
        try:
            signature = tx_data.get("signature", "pumpfun_sig")
            slot = tx_data.get("slot", 300000000)
            account_keys = tx_data.get("transaction", {}).get("message", {}).get("accountKeys", [])
            
            mint = account_keys[0] if len(account_keys) > 0 else "PumpToken11111111111111111111111111111111"
            bonding_curve = account_keys[2] if len(account_keys) > 2 else "BondingCurve11111111111111111111111111111"

            return PoolCreationEvent(
                dex=DexProtocol.PUMPFUN,
                pool_id=bonding_curve,
                base_mint=mint,
                quote_mint="So11111111111111111111111111111111111111112",
                initial_sol_liquidity=30.0,
                tx_signature=signature,
                slot=slot
            )
        except Exception:
            return None
