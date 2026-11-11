# 📝 Changelog

All notable changes to **Solana-Jito-Sniper-Engine** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-11-11
### Added
- Real-time pool decoders for Raydium AMM V4, Raydium CPMM, and Pump.fun bonding curves.
- Microsecond (< 5ms) on-chain rug-check & honeypot safety audit filter (mint/freeze authority checks, LP burn verification).
- Jito MEV block engine bundle builder with dynamic tip ladder (50th, 75th, 95th percentiles).
- Anti-sandwich attack protection via private validator mempool routing.
- Rich terminal CLI interface with simulated dry-run benchmarking (`python cli.py demo`).
- Containerized Docker & docker-compose service configuration.
- GitHub Actions continuous integration workflow and governance guidelines.
