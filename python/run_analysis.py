"""
run_analysis.py

Runs the SQL analysis queries against football_data_market.db, prints results
for verification, and exports Tableau-ready CSVs (denormalized/flat tables --
Tableau works best off flat extracts rather than a normalized schema).
"""

import sqlite3
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "football_data_market.db"
TABLEAU_DIR = BASE_DIR / "tableau"
TABLEAU_DIR.mkdir(parents=True, exist_ok=True)


def run_and_print(conn, label, query):
    print(f"\n{'=' * 70}\n{label}\n{'=' * 70}")
    cur = conn.execute(query)
    cols = [d[0] for d in cur.description]
    print(" | ".join(cols))
    for row in cur.fetchall():
        print(" | ".join(str(v) for v in row))


def export_csv(conn, query, filename):
    cur = conn.execute(query)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    out_path = TABLEAU_DIR / filename
    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(cols)
        writer.writerows(rows)
    print(f"Exported {out_path} ({len(rows)} rows)")


def main():
    conn = sqlite3.connect(DB_PATH)

    # ---- verification: run each analysis query and print ----
    queries = {
        "1. Segment leaders": """
            SELECT ds.segment_name, c.company_name, css.est_share_pct, css.basis_note
            FROM company_segment_share css
            JOIN companies c ON c.company_id = css.company_id
            JOIN data_segments ds ON ds.segment_id = css.segment_id
            WHERE css.est_share_pct = (
                SELECT MAX(css2.est_share_pct) FROM company_segment_share css2
                WHERE css2.segment_id = css.segment_id
            )
            ORDER BY css.est_share_pct DESC;
        """,
        "2. Market fragmentation (segments with >=10% players)": """
            SELECT ds.segment_name, COUNT(*) AS companies_with_meaningful_share,
                   ROUND(SUM(css.est_share_pct), 1) AS total_pct_accounted_for
            FROM company_segment_share css
            JOIN data_segments ds ON ds.segment_id = css.segment_id
            WHERE css.est_share_pct >= 10
            GROUP BY ds.segment_name
            ORDER BY companies_with_meaningful_share DESC;
        """,
        "3. Cross-segment players": """
            SELECT c.company_name, COUNT(DISTINCT css.segment_id) AS segments_active_in,
                   GROUP_CONCAT(ds.segment_name, ' | ') AS segments
            FROM company_segment_share css
            JOIN companies c ON c.company_id = css.company_id
            JOIN data_segments ds ON ds.segment_id = css.segment_id
            GROUP BY c.company_name
            ORDER BY segments_active_in DESC;
        """,
        "4. Regional coverage gaps (none/unknown)": """
            SELECT c.company_name, r.region_name, rc.coverage_status, rc.note
            FROM regional_coverage rc
            JOIN companies c ON c.company_id = rc.company_id
            JOIN regions r ON r.region_id = rc.region_id
            WHERE rc.coverage_status IN ('none', 'unknown')
            ORDER BY r.region_name, c.company_name;
        """,
        "5. Regional coverage summary": """
            SELECT r.region_name, COUNT(*) AS companies_tracked,
                   SUM(CASE WHEN rc.coverage_status IN ('full','partial') THEN 1 ELSE 0 END) AS companies_present,
                   ROUND(100.0 * SUM(CASE WHEN rc.coverage_status IN ('full','partial') THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_companies_present
            FROM regional_coverage rc
            JOIN regions r ON r.region_id = rc.region_id
            GROUP BY r.region_name
            ORDER BY pct_companies_present ASC;
        """,
        "6. Implied CAGR (2026-2031)": """
            WITH bounds AS (SELECT MIN(year) AS start_year, MAX(year) AS end_year FROM market_size)
            SELECT b.start_year, ms_start.market_size_usd_bn AS start_value_bn,
                   b.end_year, ms_end.market_size_usd_bn AS end_value_bn,
                   ROUND((POWER(ms_end.market_size_usd_bn / ms_start.market_size_usd_bn, 1.0/(b.end_year-b.start_year)) - 1) * 100, 2) AS implied_cagr_pct
            FROM bounds b
            JOIN market_size ms_start ON ms_start.year = b.start_year
            JOIN market_size ms_end ON ms_end.year = b.end_year;
        """,
        "7. Partnership timeline": """
            SELECT c.company_name, p.partner_name, p.scope, p.start_year, p.end_year
            FROM partnerships p
            JOIN companies c ON c.company_id = p.company_id
            WHERE p.end_year IS NOT NULL
            ORDER BY p.end_year ASC;
        """,
    }

    for label, q in queries.items():
        run_and_print(conn, label, q)

    # ---- Tableau exports (flat, denormalized) ----
    print(f"\n{'=' * 70}\nExporting Tableau CSVs\n{'=' * 70}")

    export_csv(conn, """
        SELECT c.company_name, c.ownership_type, c.hq_country, c.founded_year,
               c.primary_model, ds.segment_name, css.est_share_pct, css.basis_note
        FROM company_segment_share css
        JOIN companies c ON c.company_id = css.company_id
        JOIN data_segments ds ON ds.segment_id = css.segment_id
        ORDER BY ds.segment_name, css.est_share_pct DESC;
    """, "segment_shares_flat.csv")

    export_csv(conn, """
        SELECT c.company_name, c.ownership_type, r.region_name, rc.coverage_status, rc.note
        FROM regional_coverage rc
        JOIN companies c ON c.company_id = rc.company_id
        JOIN regions r ON r.region_id = rc.region_id
        ORDER BY r.region_name, c.company_name;
    """, "regional_coverage_flat.csv")

    export_csv(conn, """
        SELECT c.company_name, p.partner_name, p.scope, p.start_year, p.end_year, p.source_url
        FROM partnerships p
        JOIN companies c ON c.company_id = p.company_id
        ORDER BY p.start_year;
    """, "partnerships_flat.csv")

    export_csv(conn, "SELECT year, market_size_usd_bn, is_projection, source FROM market_size ORDER BY year;",
                "market_size.csv")

    export_csv(conn, """
        SELECT company_name, parent_group, ownership_type, hq_country, founded_year, primary_model
        FROM companies ORDER BY company_name;
    """, "companies.csv")

    conn.close()
    print("\nDone.")


if __name__ == "__main__":
    main()
