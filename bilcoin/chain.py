from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Dict, List

SATOSHIS = 100_000_000
INITIAL_BLOCK_REWARD = 50 * SATOSHIS
HALVING_INTERVAL = 210_000
MAX_SUPPLY = 21_000_000 * SATOSHIS


@dataclass(frozen=True)
class TransactionInput:
    txid: str
    output_index: int


@dataclass(frozen=True)
class TransactionOutput:
    address: str
    amount: int


@dataclass(frozen=True)
class Transaction:
    inputs: List[TransactionInput]
    outputs: List[TransactionOutput]

    def txid(self) -> str:
        payload = {
            "inputs": [vars(i) for i in self.inputs],
            "outputs": [vars(o) for o in self.outputs],
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


@dataclass
class Block:
    index: int
    previous_hash: str
    nonce: int
    difficulty: int
    transactions: List[Transaction]

    def hash(self) -> str:
        payload = {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "difficulty": self.difficulty,
            "transactions": [tx.txid() for tx in self.transactions],
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


class BilcoinChain:
    """Minimal Bitcoin-like chain prototype (educational, not production-ready)."""

    def __init__(self, difficulty: int = 4) -> None:
        self.difficulty = difficulty
        self.chain: List[Block] = []
        self.utxos: Dict[str, TransactionOutput] = {}
        self.total_issued = 0
        self._create_genesis_block()

    def _create_genesis_block(self) -> None:
        genesis_tx = Transaction(inputs=[], outputs=[TransactionOutput("genesis", 0)])
        genesis = Block(
            index=0,
            previous_hash="0" * 64,
            nonce=0,
            difficulty=self.difficulty,
            transactions=[genesis_tx],
        )
        self.chain.append(genesis)

    def block_reward(self, height: int) -> int:
        halvings = height // HALVING_INTERVAL
        reward = INITIAL_BLOCK_REWARD >> halvings
        return reward if reward > 0 else 0

    def mine_block(self, miner_address: str, transactions: List[Transaction] | None = None) -> Block:
        txs = transactions[:] if transactions else []
        height = len(self.chain)
        reward = self.block_reward(height)

        if self.total_issued + reward > MAX_SUPPLY:
            reward = max(0, MAX_SUPPLY - self.total_issued)

        coinbase = Transaction(inputs=[], outputs=[TransactionOutput(miner_address, reward)])
        txs.insert(0, coinbase)

        previous_hash = self.chain[-1].hash()
        candidate = Block(
            index=height,
            previous_hash=previous_hash,
            nonce=0,
            difficulty=self.difficulty,
            transactions=txs,
        )

        target = "0" * self.difficulty
        while not candidate.hash().startswith(target):
            candidate.nonce += 1

        self._apply_block(candidate)
        self.chain.append(candidate)
        return candidate

    def _apply_block(self, block: Block) -> None:
        for tx in block.transactions:
            txid = tx.txid()
            if tx.inputs:
                total_in = 0
                for txin in tx.inputs:
                    key = f"{txin.txid}:{txin.output_index}"
                    if key not in self.utxos:
                        raise ValueError("Invalid spend: missing UTXO")
                    total_in += self.utxos[key].amount
                    del self.utxos[key]
                total_out = sum(o.amount for o in tx.outputs)
                if total_out > total_in:
                    raise ValueError("Invalid spend: outputs exceed inputs")
            else:
                minted = sum(o.amount for o in tx.outputs)
                self.total_issued += minted

            for i, out in enumerate(tx.outputs):
                self.utxos[f"{txid}:{i}"] = out

    def create_transaction(self, from_address: str, to_address: str, amount: int) -> Transaction:
        if amount <= 0:
            raise ValueError("Amount must be positive")

        selected = []
        running_total = 0
        for key, out in self.utxos.items():
            if out.address == from_address:
                txid, index = key.split(":")
                selected.append((TransactionInput(txid, int(index)), out.amount))
                running_total += out.amount
                if running_total >= amount:
                    break

        if running_total < amount:
            raise ValueError("Insufficient funds")

        inputs = [i for i, _ in selected]
        outputs = [TransactionOutput(to_address, amount)]
        change = running_total - amount
        if change > 0:
            outputs.append(TransactionOutput(from_address, change))

        return Transaction(inputs=inputs, outputs=outputs)

    def balance(self, address: str) -> int:
        return sum(utxo.amount for utxo in self.utxos.values() if utxo.address == address)
