# Experiment snapshot (snapshot v2)

The frozen database every experiment of the paper runs on: `pg_dump -Fc` of `argus_snapshot`,
with the real site names (the anonymised copy is in the HeriKGQA repository). 1,677,556 readings,
5,227,617 observations, 71 nodes at five sites, 159 policies; data from 13 May to 12 August 2026
(09:15 UTC). Built by `scripts/snapshot_add_lorawan.py` from `argus_postgres_20261001_180439.dump`.

Split into parts below GitHub's 100 MB file limit. Reassemble, check and restore into the
Postgres of `obda/docker-compose.yml` (`ontop_snapshot` serves it on :8082):

    cat data/argus_snapshot_v2.dump.part* > data/argus_snapshot_v2.dump
    sha256sum -c data/SHA256SUMS
    createdb -h localhost -U argus argus_snapshot
    pg_restore -h localhost -U argus -d argus_snapshot --no-owner --no-privileges data/argus_snapshot_v2.dump

The experiments keep the database read-only (`ALTER DATABASE argus_snapshot SET
default_transaction_read_only = on; ... SET statement_timeout = '120s';`); the dump does not carry
these settings.
