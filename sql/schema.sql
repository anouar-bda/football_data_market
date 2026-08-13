-- ============================================================
-- Football Data Market Landscape — Schema
-- SQLite (portable; same DDL works with minor tweaks on Postgres/MySQL)
-- ============================================================

DROP TABLE IF EXISTS company_segment_share;
DROP TABLE IF EXISTS partnerships;
DROP TABLE IF EXISTS regional_coverage;
DROP TABLE IF EXISTS market_size;
DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS data_segments;
DROP TABLE IF EXISTS regions;

-- ------------------------------------------------------------
-- Reference tables
-- ------------------------------------------------------------

CREATE TABLE companies (
    company_id      INTEGER PRIMARY KEY,
    company_name    TEXT NOT NULL UNIQUE,
    parent_group    TEXT,                    -- e.g. 'Hudl' owns StatsBomb, Wyscout
    ownership_type  TEXT NOT NULL CHECK (ownership_type IN ('public','private')),
    hq_country      TEXT,
    founded_year    INTEGER,
    primary_model   TEXT NOT NULL            -- short description of core business model
);

CREATE TABLE data_segments (
    segment_id      INTEGER PRIMARY KEY,
    segment_name    TEXT NOT NULL UNIQUE,    -- e.g. 'Statistical / Event Data'
    segment_desc    TEXT
);

CREATE TABLE regions (
    region_id       INTEGER PRIMARY KEY,
    region_name     TEXT NOT NULL UNIQUE
);

-- ------------------------------------------------------------
-- Fact / relationship tables
-- ------------------------------------------------------------

-- Estimated share of each data-type segment held by each company.
-- IMPORTANT (methodology note): these are *adoption/partnership-based estimates*,
-- not revenue shares. Only Genius Sports (public, NYSE: GENI) discloses financials;
-- every other company here is private. basis_note documents how each estimate
-- was derived so the number is defensible, not invented.
CREATE TABLE company_segment_share (
    id              INTEGER PRIMARY KEY,
    company_id      INTEGER NOT NULL REFERENCES companies(company_id),
    segment_id      INTEGER NOT NULL REFERENCES data_segments(segment_id),
    est_share_pct   REAL NOT NULL CHECK (est_share_pct >= 0 AND est_share_pct <= 100),
    basis_note      TEXT NOT NULL,           -- how the estimate was derived
    source_url      TEXT
);

CREATE TABLE partnerships (
    partnership_id  INTEGER PRIMARY KEY,
    company_id      INTEGER NOT NULL REFERENCES companies(company_id),
    partner_name    TEXT NOT NULL,           -- e.g. 'Football DataCo', 'FIFA'
    scope           TEXT,                    -- what rights/data it covers
    start_year      INTEGER,
    end_year        INTEGER,
    source_url      TEXT
);

CREATE TABLE regional_coverage (
    id              INTEGER PRIMARY KEY,
    company_id      INTEGER NOT NULL REFERENCES companies(company_id),
    region_id       INTEGER NOT NULL REFERENCES regions(region_id),
    coverage_status TEXT NOT NULL CHECK (coverage_status IN ('full','partial','none','unknown')),
    note            TEXT
);

CREATE TABLE market_size (
    year                INTEGER PRIMARY KEY,
    market_size_usd_bn  REAL NOT NULL,
    is_projection       INTEGER NOT NULL DEFAULT 0,  -- 0 = reported, 1 = forecast
    source              TEXT
);
