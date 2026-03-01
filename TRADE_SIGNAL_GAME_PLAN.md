# Trade Signal Arena Plan (TradingView → BestchatVP, No Git Dependency)

## Short answer
Yes — you can build this now.

You can:
1. Generate signals in TradingView (Pine Script alerts).
2. Send alerts to your backend webhook.
3. Convert them into only **BUY / SELL / HOLD / STOP**.
4. Show the signals only inside BestchatVP.
5. Make it feel like a live sports game with rankings and audience activity.

> This plan does **not** require Git/GitHub integration to run the product.

---

## Product vision
A live signal arena where people watch top markets and top traders like a sport.

### Supported market groups
- Crypto (BTC, ETH, SOL, etc.)
- Futures (ES, NQ, CL, GC, etc.)
- Stocks (AAPL, NVDA, TSLA, etc.)
- Commodities (Gold, Oil, Silver, Natural Gas)
- Forex (EURUSD, GBPUSD, USDJPY, etc.)

### Only these states in UI
- **BUY**
- **SELL**
- **HOLD**
- **STOP**

No strategy internals need to be shown to users.

---

## System architecture

```text
TradingView Alerts (Pine Script)
        │
        │ webhook JSON
        ▼
BestchatVP API: /api/signals/tradingview
        │
        ├─ Validate secret/signature
        ├─ Normalize symbol + market type
        ├─ Deduplicate + rate limit
        ├─ Map to BUY/SELL/HOLD/STOP
        └─ Persist + publish
        ▼
Data layer (Postgres + Redis)
        │
        ├─ Live feed stream
        ├─ Leaderboards/streaks
        └─ Paper PnL engine
        ▼
BestchatVP app UI (feed + arena + profiles)
```

---

## TradingView alert format (recommended)

Use strict JSON in TradingView alert message:

```json
{
  "provider": "tradingview",
  "strategy_id": "tv_momentum_v1",
  "trader_id": "desk_alpha",
  "symbol": "BINANCE:BTCUSDT",
  "asset_class": "crypto",
  "timeframe": "15m",
  "action": "BUY",
  "price": 67123.45,
  "stop_price": 66200.0,
  "take_profit": 68900.0,
  "confidence": 0.78,
  "timestamp": "{{timenow}}",
  "nonce": "{{bar_index}}",
  "secret": "<SHARED_SECRET>"
}
```

### App mapping rule
- If action is `BUY` -> show `BUY`
- If action is `SELL` -> show `SELL`
- If action is `HOLD` -> show `HOLD`
- If action is `STOP` -> show `STOP`
- Unknown action -> reject/log (do not display)

---

## Backend endpoint behavior
`POST /api/signals/tradingview`

Validation pipeline:
1. Verify `secret` (or HMAC header).
2. Verify required fields (`strategy_id`, `trader_id`, `symbol`, `action`, `timestamp`, `nonce`).
3. Build idempotency key: `strategy_id:symbol:timeframe:timestamp:nonce`.
4. Reject duplicates.
5. Normalize symbol for UI display (e.g., `BINANCE:BTCUSDT` -> `BTC/USDT`).
6. Store event, publish to real-time feed.

Response:
- `200` accepted.
- `401` invalid auth.
- `422` schema/action invalid.
- `409` duplicate.

---

## Sports/game experience
- **Arena screen**: live market cards and signal momentum.
- **Trader profiles**: track each trader's signal history.
- **Leaderboard**: score, win rate, drawdown, consistency.
- **Streaks**: hot/cold runs.
- **Season mode**: weekly and monthly competitions.
- **Follow + alerts**: users subscribe to traders/markets.

### Example scoring model
`score = pnl_points + consistency_bonus - drawdown_penalty - spam_penalty`

---

## Paper-trading first (safer rollout)
Launch sequence:
1. Signals + watch-only experience.
2. Paper trading + public stats.
3. Optional broker execution later (region by region).

This reduces legal and operational risk while proving product engagement.

---

## Compliance essentials
Before real-money execution:
- Local investment-advice rules review.
- KYC/AML requirements.
- Broker and derivatives licensing checks.
- Risk disclosures and suitability controls.

---

## Minimal schema

### `signals`
- `id`
- `trader_id`
- `strategy_id`
- `symbol_raw`
- `symbol_display`
- `asset_class`
- `timeframe`
- `action_raw`
- `display_action` (`BUY`/`SELL`/`HOLD`/`STOP`)
- `price`
- `stop_price`
- `take_profit`
- `confidence`
- `received_at`
- `source_payload_json`

### `trader_scores`
- `trader_id`
- `period`
- `wins`
- `losses`
- `win_rate`
- `net_points`
- `max_drawdown`
- `consistency`
- `rank`

---

## 14-day MVP build checklist

### Week 1
- [ ] Create webhook endpoint.
- [ ] Add secret validation + dedupe.
- [ ] Add action mapping to BUY/SELL/HOLD/STOP.
- [ ] Save signals in DB.
- [ ] Build simple live feed API.

### Week 2
- [ ] Add live feed UI in app.
- [ ] Add trader profile page.
- [ ] Add leaderboard and streak counter.
- [ ] Add push notifications for followed traders.
- [ ] Deploy and monitor signal latency/errors.

---

## Final recommendation
Build the **watch-first signal arena** immediately with TradingView webhooks and paper stats.
It fits your idea of a large spectator trading game and can later expand into execution once compliance is ready.
