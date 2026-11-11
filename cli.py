"""
Solana-Jito-Sniper-Engine: Interactive Command Line Interface (CLI)
Provides real-time simulation runs, pool monitoring benchmarks, and token security checks.
"""

import asyncio
import argparse
from datetime import datetime
from rich.console import Console
from src.models.events import PoolCreationEvent, DexProtocol
from src.engine.sniper import SolanaSniperEngine
from src.security.honeypot_filter import HoneypotFilter

console = Console()


async def run_simulation_demo():
    console.print("\n[bold cyan]⚡ Running Solana Jito MEV Sniper Simulation Demo[/bold cyan]\n")
    engine = SolanaSniperEngine(min_liquidity_sol=5.0, snipe_amount_sol=0.2, simulation_mode=True)

    # 1. Simulate Raydium Pool Launch
    event_raydium = PoolCreationEvent(
        dex=DexProtocol.RAYDIUM_AMM_V4,
        pool_id="RaydiumPool5qXW9yZz4444444444444444444444444444",
        base_mint="SolAlpha111111111111111111111111111111111111",
        quote_mint="So11111111111111111111111111111111111111112",
        initial_sol_liquidity=25.0,
        tx_signature="5JitoSignatureRaydium111111111111111111111111111111111111111111111111",
        slot=314500120
    )
    await engine.evaluate_and_snipe(event_raydium)

    console.print("\n" + "-"*60 + "\n")

    # 2. Simulate Pump.fun Bonding Curve Creation
    event_pump = PoolCreationEvent(
        dex=DexProtocol.PUMPFUN,
        pool_id="PumpBondingCurve88888888888888888888888888888",
        base_mint="MoonTokenPumpFun1111111111111111111111111111",
        quote_mint="So11111111111111111111111111111111111111112",
        initial_sol_liquidity=30.0,
        tx_signature="3PumpFunSignature222222222222222222222222222222222222222222222222",
        slot=314500125
    )
    await engine.evaluate_and_snipe(event_pump)


def main():
    parser = argparse.ArgumentParser(description="Solana Jito Sniper CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("demo", help="Run Jito MEV sub-millisecond sniper simulation")
    
    audit_p = subparsers.add_parser("audit", help="Audit token mint for honeypot and rug vectors")
    audit_p.add_argument("--mint", "-m", required=True, help="Token contract address")

    args = parser.parse_args()

    if args.command == "audit":
        res = HoneypotFilter.audit_token(token_mint=args.mint, mint_authority=None, freeze_authority=None)
        console.print(f"\n[bold]Token Security Report for {args.mint}:[/bold]")
        console.print(f"  Passed All Filters: [bold green]{res.passed_safety_filters}[/bold green]")
        console.print(f"  Mint Revoked: {res.mint_authority_disabled}")
        console.print(f"  Freeze Revoked: {res.freeze_authority_disabled}")
        console.print(f"  LP Burned: {res.lp_burn_pct}%\n")
    else:
        asyncio.run(run_simulation_demo())


if __name__ == "__main__":
    main()
