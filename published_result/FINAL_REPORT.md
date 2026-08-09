# FRESH50 Independent Raw-Candle Research

## Final verdict

**Historical gate: FAIL**

This run used fresh Binance raw 5m candles. It did not import any old engine
PREENTRY/candidate/result rows and did not use symbol-specific tuning.

## Entry model

- Signal: completed 15m candle only.
- Planned price: that completed candle close.
- Fill proxy: first 5m open at the signal close must be exact-or-better.
- Historical fill price: planned price (better gap is not credited).
- Missed price: canceled forever; no delayed retrace.
- Original SL/TP remain fixed.
- Same 5m bar touching SL and TP is counted as SL first.

## Chronological metrics

| period        |   cost_bps |   trades |   wins |   losses |   accuracy_pct |   target_hit_rate_pct |   profit_factor |   expectancy_r |   net_r |   max_drawdown_r |   trades_per_30d |   fill_rate_pct |   symbols |   wilson95_low_pct |   wilson95_high_pct |
|:--------------|-----------:|---------:|-------:|---------:|---------------:|----------------------:|----------------:|---------------:|--------:|-----------------:|-----------------:|----------------:|----------:|-------------------:|--------------------:|
| train         |         12 |       20 |     20 |        0 |            100 |                   100 |             inf |        1.31341 | 26.2683 |                0 |         2.73973  |             100 |        15 |            83.8875 |                 100 |
| validation    |         12 |        2 |      2 |        0 |            100 |                   100 |             inf |        1.265   |  2.53   |                0 |         0.821918 |             100 |         2 |            34.238  |                 100 |
| holdout       |         12 |        0 |      0 |        0 |            nan |                   nan |             nan |      nan       |  0      |                0 |         0        |               0 |         0 |           nan      |                 nan |
| holdout_20bps |         20 |        0 |      0 |        0 |            nan |                   nan |             nan |      nan       |  0      |                0 |         0        |               0 |         0 |           nan      |                 nan |
| holdout_30bps |         30 |        0 |      0 |        0 |            nan |                   nan |             nan |      nan       |  0      |                0 |         0        |               0 |         0 |           nan      |                 nan |
| latest_30d    |         12 |        0 |      0 |        0 |            nan |                   nan |             nan |      nan       |  0      |                0 |         0        |               0 |         0 |           nan      |                 nan |

## Universe and causality

- Exact symbols: 50/50
- Candle-cut sampled rows: 16
- Candle-cut mismatches: 0
- Current-liquid static basket was used; this does not remove survivorship bias.
- Historical trade-print/5m-open proxy cannot prove real FOK order-book depth.

## Deployment

- Mainnet: **HARD BLOCKED**.
- Historical PASS, if present, allows only a separate Binance Demo forward test.
- Demo acceptance requires at least 40 actual filled and resolved trades,
  accuracy >=60%, positive after-fee expectancy, zero late/retrace entries,
  and zero unprotected positions.
