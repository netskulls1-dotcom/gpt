# R123 Point 2C — Official Archive Preflight

- Release: **V20978 R123**
- Units: **1176/1200 available**
- Point 2C status: **PREFLIGHT_FAIL_CLOSED_MISSING_OR_FAILED**
- Full acquisition allowed: **False**
- Thomas/LC-2B executed: **NO**
- Strategy core changed: **NO**
- Partial-basket accuracy: **BLOCKED**

## Status counts

- `AVAILABLE`: **1176**
- `UNAVAILABLE_OFFICIAL_404`: **24**

## Symbols with unavailable/failed units

- `BTWUSDT`: **12** non-available — `{"AVAILABLE": 12, "UNAVAILABLE_OFFICIAL_404": 12}`
- `REUSDT`: **12** non-available — `{"AVAILABLE": 12, "UNAVAILABLE_OFFICIAL_404": 12}`

## Locked consequence

The frozen basket is not silently changed. Any official 404/network/integrity unit blocks the exact 50-symbol accuracy run until the basket/window policy is explicitly changed.
