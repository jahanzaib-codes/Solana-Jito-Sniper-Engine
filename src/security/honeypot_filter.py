"""
Solana-Jito-Sniper-Engine: Rug-Check & Honeypot Filter
Evaluates on-chain token authorities, liquidity lock, and holder distribution in < 5ms.
"""

from typing import Dict, Any, Optional
from src.models.events import TokenSecurityAudit


class HoneypotFilter:
    """Evaluates Solana token safety to prevent sniping rugpulls or honeypots."""

    @staticmethod
    def audit_token(
        token_mint: str,
        mint_authority: Optional[str] = None,
        freeze_authority: Optional[str] = None,
        lp_burn_pct: float = 100.0,
        top10_holder_pct: float = 12.0
    ) -> TokenSecurityAudit:
        """
        Runs comprehensive anti-rug validation:
        1. Mint authority must be null (cannot mint more supply).
        2. Freeze authority must be null (cannot freeze trader wallets).
        3. LP burn percentage must be >= 90%.
        4. Top 10 holders must own < 30% of total circulating supply.
        """
        mint_disabled = (mint_authority is None or mint_authority == "")
        freeze_disabled = (freeze_authority is None or freeze_authority == "")
        lp_secure = lp_burn_pct >= 90.0
        concentration_safe = top10_holder_pct <= 30.0

        reasons = []
        if not mint_disabled:
            reasons.append(f"Mint authority active: {mint_authority}")
        if not freeze_disabled:
            reasons.append(f"Freeze authority active: {freeze_authority}")
        if not lp_secure:
            reasons.append(f"Liquidity pool not burned (only {lp_burn_pct}% burned)")
        if not concentration_safe:
            reasons.append(f"High whale concentration: Top 10 hold {top10_holder_pct}%")

        passed = mint_disabled and freeze_disabled and lp_secure and concentration_safe
        is_honeypot = not freeze_disabled or not mint_disabled

        return TokenSecurityAudit(
            token_mint=token_mint,
            is_honeypot=is_honeypot,
            mint_authority_disabled=mint_disabled,
            freeze_authority_disabled=freeze_disabled,
            lp_burn_pct=lp_burn_pct,
            top10_holder_pct=top10_holder_pct,
            passed_safety_filters=passed,
            rejection_reason=" | ".join(reasons) if reasons else None
        )
