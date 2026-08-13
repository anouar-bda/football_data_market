"""
build_database.py

Builds football_data_market.db (SQLite) from the schema in sql/schema.sql
and loads it with the researched dataset below.

Data provenance: every row here traces back to a specific public source
(market research reports, company newsrooms, product pages) gathered and
cited in the accompanying README / dashboard footer. Company-segment share
values are explicitly ESTIMATES derived from adoption/partnership signals,
not disclosed revenue -- see each row's basis_note. This keeps the project
honest per the "no invented data, document assumptions" standard: numbers
that can't be sourced are flagged as estimates, not presented as fact.
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "football_data_market.db"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"

DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def build_schema(conn: sqlite3.Connection) -> None:
    with open(SCHEMA_PATH, "r") as f:
        conn.executescript(f.read())


def load_reference_data(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()

    # --- companies -------------------------------------------------
    companies = [
        (1, "Stats Perform (Opta)", None, "private", "USA/UK", 1996,
         "Official statistical/event data provider; AI-driven data products; licenses to media & betting"),
        (2, "Hudl", "Hudl", "private", "USA", 2006,
         "Video analysis + scouting workflow platform; consolidated StatsBomb and Wyscout under one roof"),
        (3, "StatsBomb", "Hudl", "private", "UK", 2018,
         "Advanced event data (~3,400 events/match) and xG models; acquired by Hudl in 2024"),
        (4, "Wyscout", "Hudl", "private", "Italy", 2004,
         "Video scouting + positional data platform; acquired by Hudl in 2023"),
        (5, "Genius Sports", None, "public", "UK", 2001,
         "Official live betting-data distribution; sub-second odds feeds to sportsbooks; NYSE: GENI"),
        (6, "Sportradar", None, "public", "Switzerland", 2001,
         "Betting-data distribution and sports integrity services; competing rights holder to Genius Sports"),
        (7, "SkillCorner", None, "private", "France", 2018,
         "Broadcast-camera-based tracking data; no wearables required; open-data releases"),
        (8, "Catapult", None, "public", "Australia", 2006,
         "GPS/wearable tracking; live training-ground data and automated reporting (OpenField)"),
        (9, "Transfermarkt", None, "private", "Germany", 2000,
         "Crowd-estimated market values, transfer and squad data; free-access alternative"),
    ]
    cur.executemany(
        "INSERT INTO companies (company_id, company_name, parent_group, ownership_type, hq_country, founded_year, primary_model) "
        "VALUES (?,?,?,?,?,?,?)", companies
    )

    # --- data_segments -----------------------------------------------
    segments = [
        (1, "Statistical / Event Data", "Match events: shots, passes, pressures, xG models"),
        (2, "Video & Scouting Workflow", "Video analysis, tagging, scouting platforms"),
        (3, "Betting Data & Rights", "Official live data feeds licensed to sportsbooks"),
        (4, "Tracking / Positional Data", "Player XY tracking via broadcast cameras or wearables"),
        (5, "Transfer / Market-Value Data", "Squad, transfer fee, and market-value estimates"),
    ]
    cur.executemany(
        "INSERT INTO data_segments (segment_id, segment_name, segment_desc) VALUES (?,?,?)",
        segments
    )

    # --- regions -------------------------------------------------------
    regions = [
        (1, "Europe (major leagues)"),
        (2, "North America"),
        (3, "Asia-Pacific"),
        (4, "CAF / Continental Africa"),
        (5, "North Africa (Botola Pro / Morocco)"),
    ]
    cur.executemany("INSERT INTO regions (region_id, region_name) VALUES (?,?)", regions)

    # --- company_segment_share ------------------------------------------
    # est_share_pct: directional estimate based on adoption/partnership
    # reporting (see basis_note), NOT disclosed revenue. Documented per
    # research standards -- treat as an argued estimate, defend it as such.
    shares = [
        (1, 1, 1, 55, "Estimated from breadth of official league/federation data partnerships (incl. FIFA WC26 rights) vs. named competitors", None),
        (2, 2, 1, 30, "Estimated from StatsBomb's position as the leading alternative event-data provider post-Hudl acquisition", None),
        (3, 2, 2, 65, "Estimated from Hudl's post-Wyscout/Sportscode position as the reported standard professional-club video stack", None),
        (4, 5, 3, 50, "Based on exclusivity of Football DataCo rights (Premier League/EFL/Scottish league) through 2029", None),
        (5, 6, 3, 40, "Estimated from Sportradar's comparable scale as the other major rights holder in reported industry coverage", None),
        (6, 1, 3, 10, "Stats Perform holds FIFA World Cup 2026 betting-data rights specifically, smaller share of ongoing league rights", None),
        (7, 7, 4, 45, "Estimated from SkillCorner's positioning as leading broadcast-camera tracking specialist in industry coverage", None),
        (8, 8, 4, 35, "Estimated from Catapult's leading position in GPS/wearable training-ground tracking", None),
        (9, 9, 5, 85, "Estimated from Transfermarkt's widely reported position as the default free market-value reference used by media/agents", None),
    ]
    cur.executemany(
        "INSERT INTO company_segment_share (id, company_id, segment_id, est_share_pct, basis_note, source_url) "
        "VALUES (?,?,?,?,?,?)", shares
    )

    # --- partnerships -----------------------------------------------------
    partnerships = [
        (1, 1, "FIFA", "First official worldwide betting-data & streaming rights distributor, incl. World Cup 2026", 2026, 2026, "https://inside.fifa.com/media-releases/stats-perform-official-worldwide-betting-data-streaming-rights-distributor-world-cup"),
        (2, 5, "Football DataCo", "Exclusive live betting data + official player market data for Premier League, EFL, Scottish league", 2025, 2029, "https://www.geniussports.com/newsroom/genius-sports-and-football-dataco-extend-exclusive-official-data-partnership-through-2029/"),
        (3, 2, "StatsBomb", "Acquisition -- event data and xG models folded into Hudl platform", 2024, None, None),
        (4, 2, "Wyscout", "Acquisition -- video scouting platform folded into Hudl platform", 2023, None, None),
    ]
    cur.executemany(
        "INSERT INTO partnerships (partnership_id, company_id, partner_name, scope, start_year, end_year, source_url) "
        "VALUES (?,?,?,?,?,?,?)", partnerships
    )

    # --- regional_coverage --------------------------------------------
    # 'none' rows for North Africa are the load-bearing evidence for the
    # MENA-gap argument -- confirmed by an explicit search pass (Aug 2026)
    # that found only fan-facing score sites (Sofascore, xscores) for
    # Botola Pro, no professional data-provider partnership.
    coverage_rows = []
    region_status_by_company = {
        1: {1: "full", 2: "partial", 3: "partial", 4: "unknown", 5: "none"},
        2: {1: "full", 2: "partial", 3: "unknown", 4: "unknown", 5: "none"},
        5: {1: "full", 2: "partial", 3: "unknown", 4: "unknown", 5: "none"},
        6: {1: "full", 2: "partial", 3: "partial", 4: "unknown", 5: "none"},
        7: {1: "full", 2: "partial", 3: "unknown", 4: "unknown", 5: "none"},
        8: {1: "full", 2: "full", 3: "partial", 4: "unknown", 5: "none"},
        9: {1: "full", 2: "full", 3: "full", 4: "partial", 5: "partial"},
    }
    row_id = 1
    for company_id, region_map in region_status_by_company.items():
        for region_id, status in region_map.items():
            note = None
            if company_id != 9 and region_id == 5:
                note = "No official professional data-provider partnership found for Botola Pro as of Aug 2026 search"
            coverage_rows.append((row_id, company_id, region_id, status, note))
            row_id += 1

    cur.executemany(
        "INSERT INTO regional_coverage (id, company_id, region_id, coverage_status, note) VALUES (?,?,?,?,?)",
        coverage_rows
    )

    # --- market_size ---------------------------------------------------
    market_rows = [
        (2026, 5.28, 0, "Mordor Intelligence, Sports Analytics Market Report"),
        (2031, 17.88, 1, "Mordor Intelligence, Sports Analytics Market Report"),
    ]
    cur.executemany(
        "INSERT INTO market_size (year, market_size_usd_bn, is_projection, source) VALUES (?,?,?,?)",
        market_rows
    )

    conn.commit()


def main():
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(DB_PATH)
    try:
        build_schema(conn)
        load_reference_data(conn)
        print(f"Database built at {DB_PATH}")

        # sanity check row counts
        cur = conn.cursor()
        for table in ["companies", "data_segments", "regions",
                      "company_segment_share", "partnerships",
                      "regional_coverage", "market_size"]:
            n = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"  {table}: {n} rows")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
