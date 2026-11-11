"""
Solana-Jito-Sniper-Engine: Telemetry & Order Data Models
Defines typed schemas for on-chain pool detection, Jito bundles, and risk evaluations.
"""

from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class DexProtocol(str, Enum):
    RAYDIUM_AMM_V4 = "RAYDIUM_AMM_V4"
    RAYDIUM_CPMM = "RAYDIUM_CPMM"
    PUMPFUN = "PUMPFUN"


class BundleStatus(str, Enum):
    SUBMITTED = "SUBMITTED"
    LANDED = "LANDED"
    FAILED = "FAILED"
    DROPPED = "DROPPED"
    SIMULATED = "SIMULATED"


class PoolCreationEvent(BaseModel):
    dex: DexProtocol
    pool_id: str
    base_mint: str = Field(..., description="Target token contract address")
    quote_mint: str = Field(default="So11111111111111111111111111111111111111112", description="WSOL or USDC")
    initial_sol_liquidity: float = Field(..., ge=0.0)
    tx_signature: str
    slot: int
    timestamp: datetime = Field(default_factory=datetime.now)


class TokenSecurityAudit(BaseModel):
    token_mint: str
    is_honeypot: bool
    mint_authority_disabled: bool
    freeze_authority_disabled: bool
    lp_burn_pct: float = Field(default=100.0, ge=0.0, le=100.0)
    top10_holder_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    passed_safety_filters: bool
    rejection_reason: Optional[str] = None


class SnipeExecutionRequest(BaseModel):
    target_token: str
    amount_sol: float = Field(default=0.1, gt=0.0)
    max_slippage_bps: int = Field(default=300, ge=50, le=5000)
    jito_tip_lamports: int = Field(default=1000000, ge=10000)
    simulation_mode: bool = Field(default=True)


class JitoBundleResponse(BaseModel):
    bundle_id: str
    status: BundleStatus
    tip_lamports: int
    landed_slot: Optional[int] = None
    execution_latency_ms: float
    error_message: Optional[str] = None
