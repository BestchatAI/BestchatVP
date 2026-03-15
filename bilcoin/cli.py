from __future__ import annotations

import argparse
from bilcoin.chain import BilcoinChain, SATOSHIS


def main() -> None:
    parser = argparse.ArgumentParser(description="Bilcoin prototype chain runner")
    parser.add_argument("--difficulty", type=int, default=4)
    parser.add_argument("--mine", type=int, default=1, help="Number of blocks to mine")
    parser.add_argument("--miner", default="miner1")
    args = parser.parse_args()

    chain = BilcoinChain(difficulty=args.difficulty)
    for _ in range(args.mine):
        block = chain.mine_block(args.miner)
        print(f"Mined block {block.index} hash={block.hash()} nonce={block.nonce}")

    balance = chain.balance(args.miner) / SATOSHIS
    print(f"Miner {args.miner} balance: {balance} BIL")


if __name__ == "__main__":
    main()
