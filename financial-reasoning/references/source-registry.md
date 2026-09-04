# Source Registry

Use the highest-authority source that directly supports the claim. An API is only a transport mechanism. The publisher and methodology determine authority.

## Primary Indian Sources

| Domain | Use |
|---|---|
| `sebi.gov.in` | Securities rules, circulars, orders, investor protection |
| `investor.sebi.gov.in` | Investor education and product risk explanations |
| `rbi.org.in` | Monetary policy, banking rules, rates, consumer protection |
| `data.rbi.org.in` | Database on Indian Economy series and metadata |
| `incometax.gov.in` | Tax filing guidance and official calculators |
| `incometaxindia.gov.in` | Tax rates, rules, circulars, and notices |
| `irdai.gov.in` | Insurance rules, policyholder guidance, and complaints |
| `pfrda.org.in` | Pension regulation and NPS rules |
| `npstrust.org.in` | NPS scheme information and disclosures |
| `epfindia.gov.in` | EPF rules, balances, and interest notices |
| `dicgc.org.in` | Deposit insurance and insured-bank information |
| `mospi.gov.in` | Indian statistics, CPI, GDP, and release information |
| `indiabudget.gov.in` | Union Budget and Economic Survey |
| `data.gov.in` | Government datasets and dataset metadata |

## Market Sources

Use NSE and BSE for exchange information when access and terms permit. Use AMFI for mutual fund NAV feeds and scheme information. Use NSDL and CDSL for depository information. Use issuer documents and exchange filings for company-specific facts.

`amfiindia.com/spages/NAVAll.txt` is the primary NAV feed used by the bundled parser. `api.mfapi.in` is a community source and must be cross-checked against AMFI.

## Structured Integrations

| Integration | Authority | Use |
|---|---|---|
| World Bank API | Primary institutional publisher | Global and Indian development indicators |
| RBI DBIE | Primary Indian publisher | Indian economic and financial series |
| AMFI NAV feed | Primary industry publisher | Mutual fund NAV records |
| MFAPI | Secondary community publisher | Mutual fund discovery and historical lookup |

## Expert Explanations

Use NISM, CFA Institute, CORE Econ, university courses, IMF, World Bank, BIS, OECD, NBER, and peer-reviewed research for concepts, methods, and economic interpretation.

Use Reuters, Bloomberg, Financial Times, The Hindu, Mint, and Business Standard for event discovery and reporting context. Trace important events to the regulator, issuer, exchange, or originating institution.

## Acceptance Checks

Accept a source only when its publisher, jurisdiction, date, methodology, and scope are clear. Preserve the original source reference. Reject search snippets, anonymous claims, guaranteed-return promotions, and unsupported rankings as evidence.
