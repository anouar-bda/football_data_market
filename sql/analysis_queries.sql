-- ============================================================
-- Football Data Market Landscape — Analysis Queries
-- Run against football_data_market.db (built by python/build_database.py)
-- ============================================================

-- 1. Segment leaders: which company holds the largest estimated share
--    of each data-type segment?
SELECT
    ds.segment_name,
    c.company_name,
    css.est_share_pct,
    css.basis_note
FROM company_segment_share css
JOIN companies c       ON c.company_id = css.company_id
JOIN data_segments ds  ON ds.segment_id = css.segment_id
WHERE css.est_share_pct = (
    SELECT MAX(css2.est_share_pct)
    FROM company_segment_share css2
    WHERE css2.segment_id = css.segment_id
)
ORDER BY css.est_share_pct DESC;


-- 2. Market fragmentation check: how many distinct companies hold a
--    meaningful (>=10%) share in each segment? Low count = concentrated,
--    high count = fragmented. Used to support the "no single company
--    owns the stack" argument.
SELECT
    ds.segment_name,
    COUNT(*) AS companies_with_meaningful_share,
    ROUND(SUM(css.est_share_pct), 1) AS total_pct_accounted_for
FROM company_segment_share css
JOIN data_segments ds ON ds.segment_id = css.segment_id
WHERE css.est_share_pct >= 10
GROUP BY ds.segment_name
ORDER BY companies_with_meaningful_share DESC;


-- 3. Cross-segment players: which companies appear in more than one
--    data-type segment at all (i.e. who is actually diversifying
--    across the stack vs. staying in a single lane)?
SELECT
    c.company_name,
    COUNT(DISTINCT css.segment_id) AS segments_active_in,
    GROUP_CONCAT(ds.segment_name, ' | ') AS segments
FROM company_segment_share css
JOIN companies c      ON c.company_id = css.company_id
JOIN data_segments ds ON ds.segment_id = css.segment_id
GROUP BY c.company_name
ORDER BY segments_active_in DESC;


-- 4. Regional coverage gap: for each company, list regions with 'none'
--    or 'unknown' coverage — the core evidence for the MENA-gap argument.
SELECT
    c.company_name,
    r.region_name,
    rc.coverage_status,
    rc.note
FROM regional_coverage rc
JOIN companies c ON c.company_id = rc.company_id
JOIN regions r    ON r.region_id = rc.region_id
WHERE rc.coverage_status IN ('none', 'unknown')
ORDER BY r.region_name, c.company_name;


-- 5. Regional coverage summary: what % of tracked companies have ANY
--    presence (full or partial) in each region? Surfaces the gap at
--    a glance without reading row-by-row.
SELECT
    r.region_name,
    COUNT(*) AS companies_tracked,
    SUM(CASE WHEN rc.coverage_status IN ('full','partial') THEN 1 ELSE 0 END) AS companies_present,
    ROUND(
        100.0 * SUM(CASE WHEN rc.coverage_status IN ('full','partial') THEN 1 ELSE 0 END) / COUNT(*), 1
    ) AS pct_companies_present
FROM regional_coverage rc
JOIN regions r ON r.region_id = rc.region_id
GROUP BY r.region_name
ORDER BY pct_companies_present ASC;


-- 6. Market growth: CAGR check between first and last recorded year
--    in market_size (sanity-check against the reported 27.6% figure).
WITH bounds AS (
    SELECT
        MIN(year) AS start_year,
        MAX(year) AS end_year
    FROM market_size
)
SELECT
    b.start_year,
    ms_start.market_size_usd_bn AS start_value_bn,
    b.end_year,
    ms_end.market_size_usd_bn AS end_value_bn,
    ROUND(
        (POWER(ms_end.market_size_usd_bn / ms_start.market_size_usd_bn,
               1.0 / (b.end_year - b.start_year)) - 1) * 100
    , 2) AS implied_cagr_pct
FROM bounds b
JOIN market_size ms_start ON ms_start.year = b.start_year
JOIN market_size ms_end   ON ms_end.year   = b.end_year;


-- 7. Partnership timeline: rights deals expiring soonest — relevant for
--    "where is the market about to re-open" framing.
SELECT
    c.company_name,
    p.partner_name,
    p.scope,
    p.start_year,
    p.end_year
FROM partnerships p
JOIN companies c ON c.company_id = p.company_id
WHERE p.end_year IS NOT NULL
ORDER BY p.end_year ASC;
