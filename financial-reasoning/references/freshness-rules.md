# Freshness Rules

Static references contain concepts and procedures. They must not contain current tax slabs, market prices, interest rates, fund rankings, or regulatory conclusions.

## Required Checks

| Claim type | Required freshness |
|---|---|
| Market price or NAV | Latest available trading or valuation date |
| RBI rate or policy | Latest official RBI release |
| Tax rule or slab | Latest applicable assessment year and notification |
| Regulation | Latest circular, rule, order, or gazette |
| Macro indicator | Latest release, period, revision, and dataset vintage |
| Product feature | Current official factsheet or disclosure |
| Historical concept | Stable expert source plus current applicability check |

## Stale Data Handling

Always show the data date. Flag a source when its latest observation is older than the question requires. Weekends and market holidays can explain a delayed price, but the explanation must be stated.

Do not merge different periods, units, currencies, definitions, or revisions. If two authoritative sources disagree, show the disagreement and investigate the methodology before recommending an action.

For mutual funds, compare the newest MFAPI NAV date with the newest AMFI NAV date. AMFI is the reference source. A same-date result is current. A one-business-day gap is delayed. A gap of two or more business days is stale.

The freshness command can accept official holiday dates with repeated `--holiday YYYY-MM-DD` arguments. Without them, it uses weekends-only and marks the calendar confidence as low.

## Monitoring

The bundled script performs live reads only when invoked. A future scheduler may run source-health checks and create a review queue. It must preserve old evidence, diff new documents, classify changes, and require human review before changing static guidance.
