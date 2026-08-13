# Football Data Market Landscape — Competitive Analysis & the MENA Gap

Independent project · 2026
SQL · Python · Tableau

Anouar Lacheheb · [GitHub](https://github.com/anouar-bda) · [LinkedIn](https://www.linkedin.com/in/anouar-lacheheb-328052398) · [Portfolio](https://anouarlacheheb.com)

## Background

The football data-and-analytics industry (Opta, Hudl, StatsBomb, Genius Sports, Sportradar,
SkillCorner, Catapult, Transfermarkt) is usually described informally, company by company.
I wanted to treat it as a market to be mapped instead: who leads which data-type segment,
how fragmented the competition actually is, and — using regional coverage as the evidence —
where the market hasn't been contested yet.

## Objective

I set out to answer three questions with a reproducible SQL/Python pipeline rather than
narrative claims:

1. Which company leads each data-type segment (statistical/event data, video & scouting,
   betting data & rights, tracking/positional data, transfer/market-value data)?
2. Is the market actually fragmented, or does one company dominate across segments?
3. Which regions are well-served, and which are not — specifically, is there a real gap
   in North Africa / Morocco (Botola Pro)?

## Data & Methodology

- **Market sizing**: Mordor Intelligence Sports Analytics Market Report (2026 figure: $5.28B,
  2031 projection: $17.88B, reported CAGR 27.63%). I independently recomputed the CAGR from
  the two raw data points as a sanity check (`sql/analysis_queries.sql`, query 6) — it matched
  the reported figure exactly.
- **Company segment shares**: since only Genius Sports (NYSE: GENI) is publicly listed and
  discloses financials, every other company's segment share here is an **estimate** I derived
  from documented partnership scope and industry-adoption reporting — I'm not presenting these
  as revenue. Each estimate carries a `basis_note` in the database explaining how I derived it
  (see `company_segment_share` table).
- **Regional coverage**: built from a documented search pass (Aug 2026) checking whether each
  company has any disclosed official partnership or product presence in Europe, North America,
  Asia-Pacific, continental Africa (CAF), and North Africa specifically. For Botola Pro
  (Morocco's top division), the only sources I found were fan-facing score aggregators
  (Sofascore, xscores) — no professional data-provider partnership for any of the nine
  companies I tracked.
- **Partnerships**: sourced from company newsrooms and industry press (FIFA.com, Genius Sports
  newsroom) — see `source_url` fields in the `sql/schema.sql` data load.

## Tools

- **SQL** (SQLite) — schema design (`sql/schema.sql`), analytical queries
  (`sql/analysis_queries.sql`): segment-leader lookups, fragmentation check, cross-segment
  player identification, regional coverage gap and summary, CAGR verification, partnership
  timeline.
- **Python** (`python/build_database.py`, `python/run_analysis.py`) — builds the database,
  loads the dataset I researched with documented provenance, runs and verifies all seven
  analysis queries, exports flat Tableau-ready CSVs.
- **Tableau Public** — final interactive dashboard built from the flat exports in
  `tableau/*.csv`. Published dashboard: *[add link once published]*.

## Key Findings

- **No company spans the full data stack.** Cross-segment analysis (query 3) shows only
  Stats Perform and Hudl active in two segments each; every other company (Genius Sports,
  Sportradar, SkillCorner, Catapult, Transfermarkt) is a single-segment specialist.
- **The market is genuinely fragmented, not concentrated** — betting data & rights alone has
  three companies each holding a meaningful (≥10%) share, together accounting for 100% of the
  estimated segment.
- **Regional coverage is starkly uneven.** Europe and North America show full/partial presence
  from all 7 companies I tracked with regional data; continental Africa and North Africa
  specifically show presence from only 1 of 7 (14.3%) — Transfermarkt, via its general free
  market-value coverage, not a dedicated football-data product.
- **No official data-provider partnership for Botola Pro** across any of the nine companies I
  researched — this gap isn't inferred from the absence of a market report, it's confirmed by
  checking each company directly.

## Repository Structure

```
football_data_market/
├── README.md
├── sql/
│   ├── schema.sql
│   └── analysis_queries.sql
├── python/
│   ├── build_database.py
│   └── run_analysis.py
├── data/
│   └── football_data_market.db
└── tableau/
    ├── companies.csv
    ├── segment_shares_flat.csv
    ├── regional_coverage_flat.csv
    ├── partnerships_flat.csv
    └── market_size.csv
```

## Limitations

- Segment-share percentages are estimates, not disclosed financials, for 8 of the 9 companies
  covered — read them as "directional leadership," not precise market share. I've flagged this
  in the database itself (`basis_note` column) and I'm repeating it here deliberately, since
  it's the single most important caveat in the project.
- Regional coverage is based on a single documented search pass, not primary confirmation from
  each company (e.g. a direct inquiry to Opta or Hudl about African coverage). A stronger
  version of this project would follow up with each company directly.
- "Coverage" as I've defined it means a disclosed partnership or product presence — it doesn't
  capture whether a company's general product (e.g. Transfermarkt) is actually used by anyone
  in that region in practice.

## What I'd Do With More Time

- Reach out directly to SkillCorner, Hudl, and Opta to confirm (or correct) the North Africa
  coverage finding rather than relying on public-source absence.
- Build a small primary dataset of what data Botola Pro clubs currently do have access to (if
  any), to turn "no provider found" into "here is what exists instead."
- Extend the regional-coverage table to more African leagues beyond Morocco to see whether the
  gap is Morocco-specific or continent-wide.
