import unittest

from bilcoin.chain import (
    BilcoinChain,
    HALVING_INTERVAL,
    INITIAL_BLOCK_REWARD,
    MAX_SUPPLY,
    SATOSHIS,
)


class BilcoinChainTests(unittest.TestCase):
    def test_mining_reward_and_balance(self):
        chain = BilcoinChain(difficulty=2)
        chain.mine_block("alice")
        self.assertEqual(chain.balance("alice"), INITIAL_BLOCK_REWARD)

    def test_send_transaction_utxo(self):
        chain = BilcoinChain(difficulty=2)
        chain.mine_block("alice")
        tx = chain.create_transaction("alice", "bob", 10 * SATOSHIS)
        chain.mine_block("miner", [tx])

        self.assertEqual(chain.balance("bob"), 10 * SATOSHIS)
        expected_alice = INITIAL_BLOCK_REWARD - 10 * SATOSHIS
        self.assertEqual(chain.balance("alice"), expected_alice)

    def test_halving(self):
        chain = BilcoinChain(difficulty=1)
        self.assertEqual(chain.block_reward(0), INITIAL_BLOCK_REWARD)
        self.assertEqual(chain.block_reward(HALVING_INTERVAL), INITIAL_BLOCK_REWARD // 2)

    def test_supply_cap(self):
        chain = BilcoinChain(difficulty=1)
        chain.total_issued = MAX_SUPPLY - 1
        chain.mine_block("alice")
        self.assertEqual(chain.total_issued, MAX_SUPPLY)


if __name__ == "__main__":
    unittest.main()
