-- Postgres schema for the ARGUS observations (phase 2 of the OBDA plan).
--
-- Topology (sites/nodes/sensors/observed_properties) is small and near-static.
-- observations is the unbounded time series — the table that outgrows an
-- in-memory RDF graph. Ontop maps these tables back to the SOSA/ARGUS RDF the
-- pipeline already queries (see argus.obda), so no pipeline code changes.

CREATE TABLE IF NOT EXISTS sites (
    site_id  TEXT PRIMARY KEY,          -- sanitised site name, e.g. 'baltanas'
    label    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS nodes (
    node_id   TEXT PRIMARY KEY,
    label     TEXT,
    name      TEXT,
    model     TEXT,
    latitude  DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    altitude  DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS sensors (
    sensor_id TEXT PRIMARY KEY,
    label     TEXT,
    model     TEXT
);

CREATE TABLE IF NOT EXISTS observed_properties (
    property_id TEXT PRIMARY KEY,        -- the quantity label, e.g. 'temperature'
    label       TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS readings (
    reading_id      TEXT PRIMARY KEY,    -- reading_stable_id() hash
    result_time     TIMESTAMPTZ,
    site_id         TEXT REFERENCES sites,
    sensor_id       TEXT REFERENCES sensors,
    node_id         TEXT REFERENCES nodes,
    reading_type    TEXT,
    topic           TEXT,
    topic_id        TEXT,
    device_group_id TEXT
);

CREATE TABLE IF NOT EXISTS observations (
    observation_id TEXT PRIMARY KEY,
    reading_id     TEXT REFERENCES readings,
    property_id    TEXT REFERENCES observed_properties,
    value          DOUBLE PRECISION,     -- numeric measurements (for AVG/MIN/MAX)
    value_text     TEXT,                 -- non-numeric values (booleans, strings)
    unit           TEXT,
    result_time    TIMESTAMPTZ
);

-- The pipeline filters/aggregates by site, property and time; index accordingly.
CREATE INDEX IF NOT EXISTS readings_result_time_idx ON readings (result_time);
CREATE INDEX IF NOT EXISTS readings_site_idx        ON readings (site_id);
CREATE INDEX IF NOT EXISTS observations_reading_idx ON observations (reading_id);
CREATE INDEX IF NOT EXISTS observations_property_idx ON observations (property_id);
CREATE INDEX IF NOT EXISTS observations_time_idx     ON observations (result_time);

-- Bookkeeping for scripts/0b_online_ingest.py's live loop (e.g. last API page
-- successfully processed). Not part of the RDF the pipeline queries.
CREATE TABLE IF NOT EXISTS ingest_state (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

-- Governance data (scripts/0c_ingest_governance_pg.py, from the ARGUS API's
-- /threats, /policies, /decisions, /assets) — mirrors the panoptes:Threat/
-- Policy/Decision/Asset individuals scripts/0a_offline_readings.py's
-- ingest_governance() writes into the local TTL, via the same Ontop mapping
-- (see obda/argus.obda) so the pipeline's SPARQL is identical either way.
--
-- Mutable reference data, not an append-only event log like readings/
-- observations — 0c_ingest_governance_pg.py upserts by the API's own id
-- (ON CONFLICT ... DO UPDATE), so an edited threshold overwrites, not
-- duplicates.
--
-- site_id has no FK to sites on purpose: governance can be ingested before
-- any readings exist for a pilot (the two ingest scripts run independently),
-- so a dangling reference here is normal, not a data error — matches the RDF
-- path, where ex:site/{slug} is just a URI regardless of whether a Site
-- individual has been asserted for it yet.

CREATE TABLE IF NOT EXISTS threats (
    threat_id    TEXT PRIMARY KEY,       -- ARGUS API /threats numeric id, as text
    label        TEXT NOT NULL,
    description  TEXT,
    threat_level TEXT
);

CREATE TABLE IF NOT EXISTS policies (
    policy_id       TEXT PRIMARY KEY,    -- ARGUS API /policies numeric id, as text
    label           TEXT NOT NULL,
    description     TEXT,
    rule_id         TEXT,                -- AD-RT rule id, e.g. 'R1a_rain_1h'
    threat_name     TEXT,                -- free-text; not yet FK'd to threats.threat_id upstream
    threshold_value DOUBLE PRECISION,    -- set only when the rule has exactly one threshold param
    threshold_json  TEXT,                -- full threshold_overrides dict, always set when non-empty
    site_id         TEXT                 -- pilot slug, e.g. 'baltanas' (see sites.site_id)
);

CREATE TABLE IF NOT EXISTS decisions (
    decision_id TEXT PRIMARY KEY,        -- ARGUS API /decisions numeric id, as text
    label       TEXT NOT NULL,
    description TEXT,
    urgency     TEXT
);

CREATE TABLE IF NOT EXISTS assets (
    asset_id     TEXT PRIMARY KEY,       -- ARGUS API /assets numeric id, as text
    label        TEXT NOT NULL,
    description  TEXT,
    asset_code   TEXT,
    pilot_number INTEGER,
    country      TEXT,
    source_url   TEXT,
    site_id      TEXT                    -- pilot slug matched from asset_code/label
);

CREATE INDEX IF NOT EXISTS policies_site_idx ON policies (site_id);
CREATE INDEX IF NOT EXISTS policies_rule_idx ON policies (rule_id);
CREATE INDEX IF NOT EXISTS assets_site_idx   ON assets (site_id);

-- Scaling note: for very large deployments make observations a TimescaleDB
-- hypertable — SELECT create_hypertable('observations','result_time') — and add
-- continuous aggregates for per-site/per-property hourly stats. Plain Postgres
-- is fine to start; Ontop and the pipeline are unaffected either way.
