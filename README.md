# Bilcoin (BIL) - Bitcoin-like Coin Prototype

You asked for a **coin like Bitcoin, not a token**.

This repository now contains a **minimal standalone blockchain prototype** for Bilcoin with Bitcoin-inspired mechanics:

- Proof-of-Work mining (`sha256`, leading-zero difficulty target)
- UTXO transaction model
- Coinbase block rewards
- Reward halving schedule
- Hard-capped max supply at 21,000,000 coins
- 8 decimal places (satoshi-style units)

## Project structure

- `bilcoin/chain.py` - chain, block, UTXO, mining, reward, and supply logic
- `bilcoin/cli.py` - simple command-line miner runner
- `tests/test_bilcoin_chain.py` - unit tests for reward, UTXO spending, halving, and supply cap

## Run

```bash
python -m bilcoin.cli --difficulty 4 --mine 2 --miner bilcoin-founder
```

## Test

```bash
python -m unittest discover -s tests -v
```

## Important note

This is an educational prototype and **not production-ready mainnet software**. A real Bitcoin-class chain needs p2p networking, mempool policy, consensus-hardening, signature scripts, persistent storage, fork-choice logic, adversarial testing, and external security review.


## Want the full process?

See the complete step-by-step guide:

- `docs/full-process-guide.md`
