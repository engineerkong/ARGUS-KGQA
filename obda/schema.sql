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

-- Scaling note: for very large deployments make observations a TimescaleDB
-- hypertable — SELECT create_hypertable('observations','result_time') — and add
-- continuous aggregates for per-site/per-property hourly stats. Plain Postgres
-- is fine to start; Ontop and the pipeline are unaffected either way.
