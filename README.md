# Football Data Market Landscape
### Competitive Analysis and the North Africa Gap

![SQL](https://img.shields.io/badge/SQL-SQLite-4479A1?style=flat-square&logo=sqlite&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)
![Tableau](https://img.shields.io/badge/Tableau-Public-E97627?style=flat-square&logo=tableau&logoColor=white)
![Status](https://img.shields.io/badge/status-independent%20project-lightgrey?style=flat-square)

**Anouar Lacheheb** · [GitHub](https://github.com/anouar-bda) · [LinkedIn](https://www.linkedin.com/in/anouar-lacheheb-328052398) · [Portfolio](https://anouarlacheheb.com) · [Live Tableau Story](https://public.tableau.com/shared/7JB86XKM3?:display_count=n&:origin=viz_share_link)

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

1. Which company leads each data type segment (statistical/event data, video and scouting,
   betting data and rights, tracking/positional data, transfer/market value data)?
2. Is the market actually fragmented, or does one company dominate across segments?
3. Which regions are well served, and which are not? Specifically, is there a real gap in
   North Africa (Morocco, Algeria, Tunisia, Egypt)?

## Data and Methodology

| Area | Approach |
|---|---|
| **Market sizing** | Mordor Intelligence Sports Analytics Market Report (2026: $5.28B, 2031 projection: $17.88B, reported CAGR 27.63%). Independently recomputed the CAGR from the two raw data points as a sanity check. It matched the reported figure exactly. The Tableau trend chart shows only 2026 and 2031 as reported figures; intermediate years are modeled at the verified CAGR and labeled as such, not presented as sourced data. |
| **Company segment shares** | Only Genius Sports (NYSE: GENI) is publicly listed and discloses financials. Every other company's segment share is an **estimate** derived from documented partnership scope and industry adoption reporting, not revenue. Each estimate carries a `basis_note` in the database. Segment shares are tracked for 7 of the 9 companies in the dataset; StatsBomb and Wyscout are covered under Hudl's parent-group share rather than individually, since both were acquired into Hudl's platform. |
| **Regional coverage** | Built from multiple documented search passes (Aug 2026) checking for disclosed official partnerships or product presence across Europe, North America, Asia-Pacific, continental Africa, North Africa, and South America. Beyond the region-level defaults, over 70 countries were individually researched and recorded in a dedicated `country_overrides` table, each row documenting what was actually checked, not assumed. Rows marked "unknown" are further split into `plausible_gap` (a genuine absence is credible for that market) versus `likely_undetected` (a large or established market where a deal plausibly exists but wasn't surfaced by this project's English-language search pass) — a distinction added specifically so that not every "no result found" row reads with the same confidence. |
| **North Africa specifically** | Re-verified using French- and Arabic-context sources, not just English, given this is the project's central finding. Morocco has a confirmed Hudl partnership with the Fédération Royale Marocaine de Football (FRMF, announced April 2022): Hudl Sportscode and Wyscout training and tooling for federation and Botola Pro analysts. This is federation-level tooling, not a commercial league-wide data-provider deal of the kind Opta holds with the Premier League, so it's recorded as **partial**, not full. Algeria, Tunisia, and Egypt show no equivalent partnership with any of the nine companies researched. |
| **Partnerships** | Sourced from company newsrooms and industry press (FIFA.com, Genius Sports newsroom, Stats Perform press releases, Hudl blog). See `source_url` fields in `sql/schema.sql` and `country_overrides` rows in `python/build_database.py`. |

## Tools

1. **SQL** (SQLite): schema design (`sql/schema.sql`), analytical queries (`sql/analysis_queries.sql`). Segment leader lookups, fragmentation check, cross segment player identification, regional coverage gap and summary, CAGR verification, partnership timeline.
2. **Python** (`python/build_database.py`, `python/run_analysis.py`): builds the database, loads the researched dataset with documented provenance, runs and verifies all seven analysis queries, exports flat Tableau ready CSVs.
3. **Tableau Public**: interactive dashboards and a guided Story built from the flat exports in `tableau/*.csv`. Live version: [public.tableau.com/shared/7JB86XKM3](https://public.tableau.com/shared/7JB86XKM3?:display_count=n&:origin=viz_share_link)

## Key Findings

1. **No company spans the full data stack.** Cross segment analysis shows only Stats Perform and Hudl active in two segments each; every other tracked company is a single-segment specialist.
2. **The market is genuinely fragmented, not concentrated.** Betting data and rights is the most contested segment, with three companies each holding a meaningful share (Genius Sports 50%, Sportradar 40%, Stats Perform 10%).
3. **Regional coverage is starkly uneven.** Europe and North America show full or partial presence from all 7 companies tracked with regional data; continental Africa and North Africa show presence from only 1 of 7.
4. **North Africa has one real but limited exception, not a total gap.** Morocco has a confirmed Hudl/FRMF federation-level training partnership; Algeria, Tunisia, and Egypt have no equivalent partnership with any of the nine companies researched. Over 70 countries were individually verified to support this finding, not just the four in North Africa, so the comparison against other established and lesser-known markets is grounded in the same standard of evidence throughout.

## So What: Recommendation

A market map is only useful if it tells someone what to do differently.

**For a founder or analytics provider evaluating where to build:** North Africa isn't a "crowded market, enter carefully" situation, it's a largely unaddressed one, with one federation already showing appetite for better tooling. That does *not* mean "build a company now." The right next step is validation, not construction: talk to Botola Pro clubs, the Algerian, Tunisian, and Egyptian federations, and the Moroccan federation directly about what they actually have and would pay for, before building anything.

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
    ├── regional_coverage_map_full.csv
    ├── partnerships_flat.csv
    ├── market_size.csv
    └── market_size_trend.csv
```

`country_overrides` (individually verified countries, coverage status, and unknown-type
classification) lives in the SQLite database and in `python/build_database.py`, sourced there
rather than as a standalone CSV since it feeds directly into `regional_coverage_map_full.csv`.

## Limitations

1. Segment share percentages are **estimates**, not disclosed financials, for 8 of the 9 companies covered. Read them as directional leadership, not precise market share.
2. Regional coverage beyond the individually verified countries relies on region-level defaults from a documented search pass, not primary confirmation from each company directly.
3. "Coverage" as defined here means a disclosed partnership or product presence. It doesn't capture whether a general product (for example Transfermarkt) is actually used by anyone in that region in practice.
4. Country-level research was conducted in English by default, with French and Arabic sources used specifically for North Africa. Countries marked `likely_undetected` in the dataset may have real partnerships this project's search pass did not surface, and should not be read with the same confidence as the North Africa finding.
5. The Market Size trend chart's intermediate years (2027–2030) are modeled at the reported CAGR, not individually sourced figures.

## What I'd Do With More Time

1. Reach out directly to SkillCorner, Hudl, and Opta to confirm or correct the North Africa coverage finding, including whether Hudl has any plans to expand the FRMF relationship into a commercial league-wide deal.
2. Build a small primary dataset of what data Botola Pro, and the Algerian, Tunisian, and Egyptian top leagues currently have access to, if any.
3. Re-run the `likely_undetected` countries through non-English search passes, the same way North Africa was re-verified, to see how many resolve to real partnerships versus genuine gaps.
4. Talk to at least one club or federation in the region directly. This is the step that turns this from desk research into real validation.
