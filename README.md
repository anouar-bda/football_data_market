# Football Data Market Landscape
### Competitive Analysis and the MENA Gap


**Anouar Lacheheb** · [GitHub](https://github.com/anouar-bda) · [LinkedIn](https://www.linkedin.com/in/anouar-lacheheb-328052398) · [Portfolio](https://anouarlacheheb.com)

---

## Table of Contents

1. [Background](#background)
2. [Objective](#objective)
3. [Data and Methodology](#data-and-methodology)
4. [Tools](#tools)
5. [Key Findings](#key-findings)
6. [So What: Recommendation](#so-what-recommendation)
7. [Repository Structure](#repository-structure)
8. [Limitations](#limitations)
9. [What I'd Do With More Time](#what-id-do-with-more-time)

---

## Background

The football data and analytics industry (Opta, Hudl, StatsBomb, Genius Sports, Sportradar,
SkillCorner, Catapult, Transfermarkt) is usually described informally, company by company. I
wanted to treat it as a market to be mapped instead: **who leads which data type segment, how
fragmented the competition actually is, and where the market hasn't been contested yet.**

There's a personal reason I picked this over another club level project. I'm from Morocco, and
long term I want to build something in football data for Morocco and North Africa, not as a
vague ambition but as an actual company one day, serving clubs, academies, and federations that
currently have no real data infrastructure to work with. Before I can credibly build anything
there, I need to actually understand the industry I'd be entering: who the players are, how they
make money, and whether the gap I assume exists in the region is real, or just something I want
to be true because I'm from there. **This project is that check.**

## Objective

I set out to answer three questions with a reproducible SQL/Python pipeline rather than
narrative claims.

. Which company leads each data type segment (statistical/event data, video and scouting,
   betting data and rights, tracking/positional data, transfer/market value data)?
. Is the market actually fragmented, or does one company dominate across segments?
. Which regions are well served, and which are not? Specifically, is there a real gap in
   North Africa and Morocco (Botola Pro)?

## Data and Methodology

| Area | Approach |
|---|---|
| **Market sizing** | Mordor Intelligence Sports Analytics Market Report (2026: $5.28B, 2031 projection: $17.88B, reported CAGR 27.63%). Independently recomputed the CAGR from the two raw data points as a sanity check. It matched the reported figure exactly. |
| **Company segment shares** | Only Genius Sports (NYSE: GENI) is publicly listed and discloses financials. Every other company's segment share is an **estimate** derived from documented partnership scope and industry adoption reporting, not revenue. Each estimate carries a `basis_note` in the database. |
| **Regional coverage** | Built from a documented search pass (Aug 2026) checking for disclosed official partnerships or product presence across Europe, North America, Asia Pacific, continental Africa, and North Africa specifically. For Botola Pro, only fan facing score aggregators (Sofascore, xscores) were found. No professional data provider partnership turned up for any of the nine companies tracked. |
| **Partnerships** | Sourced from company newsrooms and industry press (FIFA.com, Genius Sports newsroom). See `source_url` fields in `sql/schema.sql`. |

## Tools

. **SQL** (SQLite): schema design (`sql/schema.sql`), analytical queries (`sql/analysis_queries.sql`). Segment leader lookups, fragmentation check, cross segment player identification, regional coverage gap and summary, CAGR verification, partnership timeline.

. **Python** (`python/build_database.py`, `python/run_analysis.py`): builds the database, loads the researched dataset with documented provenance, runs and verifies all seven analysis queries, exports flat Tableau ready CSVs.

. **Tableau Public**: final interactive dashboard built from the flat exports in `tableau/*.csv`. Published dashboard: .

## Key Findings

. **No company spans the full data stack.** Cross segment analysis shows only Stats Perform and Hudl active in two segments each; every other company is a single segment specialist.

. **The market is genuinely fragmented, not concentrated.** Betting data and rights alone has three companies each holding a meaningful (at least 10%) share.

. **Regional coverage is starkly uneven.** Europe and North America show full or partial presence from all 7 companies tracked with regional data; continental Africa and North Africa show presence from only 1 of 7 (14.3%).

. **No official data provider partnership for Botola Pro** across any of the nine companies researched, confirmed by checking each company directly, not inferred from a market report's silence.

## So What: Recommendation

A market map is only useful if it tells someone what to do differently.

**For a founder or analytics provider evaluating where to build:** North Africa isn't a "crowded market, enter carefully" situation, it's an unaddressed one. That does *not* mean "build a company now." The right next step is validation, not construction: talk to Botola Pro clubs or the Moroccan federation about what they actually have and would pay for, before building anything.

**For a club or federation in the region:** the fragmentation finding matters practically. No single vendor solves everything, so a lower budget club doesn't need a full Opta/Hudl scale package. A cheaper, narrower tool is a realistic starting point, and the segment map shows exactly which piece that would be.

**For me:** this is the first real evidence based step toward the Morocco and North Africa vision described above, and the strongest proof I have that I understand the industry I want to eventually build in, beyond being a fan of the idea.

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

. Segment share percentages are **estimates**, not disclosed financials, for 8 of the 9 companies covered. Read them as directional leadership, not precise market share.

. Regional coverage is based on a single documented search pass, not primary confirmation from each company directly.

. "Coverage" as defined here means a disclosed partnership or product presence. It doesn't capture whether a general product (for example Transfermarkt) is actually used by anyone in that region in practice.

## What I'd Do With More Time

. Reach out directly to SkillCorner, Hudl, and Opta to confirm or correct the North Africa coverage finding.

. Build a small primary dataset of what data Botola Pro clubs currently have access to, if any.

. Extend the regional coverage table to more African leagues beyond Morocco.

. Talk to at least one Botola Pro club or the Moroccan federation directly. This is the step that turns this from desk research into real validation.
