# FRESH50 Independent Raw-Candle Research v2

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

| period        |   cost_bps |   trades |   wins |   losses |   accuracy_pct |   target_hit_rate_pct |   profit_factor |   expectancy_r |     net_r |   max_drawdown_r |   trades_per_30d |   fill_rate_pct |   symbols |   wilson95_low_pct |   wilson95_high_pct |   active_months |   positive_months |   positive_month_ratio |   worst_month_accuracy_pct |   median_month_accuracy_pct |   minimum_month_trades |
|:--------------|-----------:|---------:|-------:|---------:|---------------:|----------------------:|----------------:|---------------:|----------:|-----------------:|-----------------:|----------------:|----------:|-------------------:|--------------------:|----------------:|------------------:|-----------------------:|---------------------------:|----------------------------:|-----------------------:|
| train         |         12 |     1243 |   1180 |       63 |        94.9316 |               94.9316 |       10.1069   |      0.526447  | 654.373   |          5.17541 |         170.274  |             100 |        49 |            93.5678 |             96.0186 |               8 |                 8 |               1        |                    85.1852 |                     94.7727 |                     27 |
| validation    |         12 |      117 |     83 |       34 |        70.9402 |               70.9402 |        1.23844  |      0.0798163 |   9.33851 |         11.5614  |          48.0822 |             100 |        38 |            62.1519 |             78.3971 |               3 |                 2 |               0.666667 |                    69.3333 |                     74.0606 |                      9 |
| holdout       |         12 |      110 |     57 |       53 |        51.8182 |               51.8182 |        0.57073  |     -0.23534   | -25.8874  |         30.1453  |          45.2055 |             100 |        39 |            42.5779 |             60.9357 |               4 |                 0 |               0        |                    48.9362 |                     52.3527 |                      5 |
| holdout_20bps |         20 |      110 |     57 |       53 |        51.8182 |               51.8182 |        0.442858 |     -0.330112  | -36.3123  |         38.2422  |          45.2055 |             100 |        39 |            42.5779 |             60.9357 |               4 |                 0 |               0        |                    48.9362 |                     52.3527 |                      5 |
| holdout_30bps |         30 |      110 |     57 |       53 |        51.8182 |               51.8182 |        0.307597 |     -0.448577  | -49.3434  |         50.1426  |          45.2055 |             100 |        39 |            42.5779 |             60.9357 |               4 |                 0 |               0        |                    48.9362 |                     52.3527 |                      5 |
| latest_30d    |         12 |       57 |     32 |       25 |        56.1404 |               56.1404 |        0.651518 |     -0.177323  | -10.1074  |         16.2782  |          57      |             100 |        28 |            43.278  |             68.2273 |               2 |                 0 |               0        |                    55.7692 |                     55.7692 |                      5 |

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
