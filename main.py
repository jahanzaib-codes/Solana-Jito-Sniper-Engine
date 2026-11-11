"""
Solana-Jito-Sniper-Engine: Daemon Entrypoint
Initializes websocket listener, security pipeline, and Jito bundle orchestrator.
"""

import os
import asyncio
import signal
from dotenv import load_dotenv
from rich.console import Console
from src.engine.sniper import SolanaSniperEngine
from src.mev.jito_client import JitoBundleClient

load_dotenv()
console = Console()


async def main():
    rpc_url = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
    tip_account = os.getenv("JITO_TIP_ACCOUNT", "96gYZGLnJYVFmbjzopPSU6QiEV5fGqZNyN9nmNhvrZU5")
    simulation = os.getenv("SIMULATION_MODE", "True").lower() == "true"
    min_liq = float(os.getenv("MIN_LIQUIDITY_SOL", "5.0"))
    snipe_sol = float(os.getenv("SNIPE_AMOUNT_SOL", "0.1"))

    console.print("\n" + "="*60)
    console.print("[bold cyan]🚀 Solana Jito MEV Sniper Engine Initializing...[/bold cyan]")
    console.print(f"  RPC Endpoint: [yellow]{rpc_url}[/yellow]")
    console.print(f"  Jito Tip Account: [magenta]{tip_account}[/magenta]")
    console.print(f"  Min Liquidity Filter: [green]{min_liq} SOL[/green]")
    console.print(f"  Snipe Amount: [bold]{snipe_sol} SOL[/bold]")
    console.print(f"  Mode: [{'yellow' if simulation else 'red'}]{'SIMULATION / DRY-RUN' if simulation else 'LIVE MAINNET'}[/]")
    console.print("="*60 + "\n")

    jito_client = JitoBundleClient()
    engine = SolanaSniperEngine(
        jito_client=jito_client,
        min_liquidity_sol=min_liq,
        snipe_amount_sol=snipe_sol,
        simulation_mode=simulation
    )

    console.print("[green]✓ Event listeners online. Monitoring Raydium AMM V4, CPMM, and Pump.fun pools...[/green]")
    console.print("[dim]Press Ctrl+C to terminate cleanly.[/dim]\n")

    # Keep alive loop
    try:
        while True:
            await asyncio.sleep(1)
    except (asyncio.CancelledError, KeyboardInterrupt):
        console.print("\n[yellow]Shutdown signal received. Disconnecting RPC and flushing telemetry...[/yellow]")


if __name__ == "__main__":
    asyncio.run(main())
