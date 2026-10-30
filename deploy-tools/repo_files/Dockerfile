# HeriKGQA: PostgreSQL 16 (anonymised snapshot) + Ontop 5.5 + the pipeline, in one container.
# Without a command it serves the web demo on port 7860; with one (e.g. python scripts/run_eval.py …)
# it runs that command once the SPARQL endpoint is up.
FROM postgres:16-bookworm

RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 python3-venv openjdk-17-jre-headless curl unzip ca-certificates \
 && rm -rf /var/lib/apt/lists/*

ARG ONTOP_VERSION=5.5.0
RUN curl -fsSL -o /tmp/ontop.zip \
      "https://github.com/ontop/ontop/releases/download/ontop-${ONTOP_VERSION}/ontop-cli-${ONTOP_VERSION}.zip" \
 && mkdir -p /opt/ontop && unzip -q /tmp/ontop.zip -d /opt/ontop && rm /tmp/ontop.zip \
 && chmod +x /opt/ontop/ontop

RUN useradd -m -u 1000 user && chown -R user /opt/ontop/jdbc
USER user
ENV HOME=/home/user \
    PATH=/home/user/venv/bin:/usr/lib/postgresql/16/bin:$PATH \
    PGDATA=/home/user/pgdata \
    PYTHONUNBUFFERED=1
WORKDIR /home/user/herikgqa

COPY --chown=user requirements.txt .
RUN python3 -m venv /home/user/venv && pip install --no-cache-dir -r requirements.txt

COPY --chown=user . .

# Benchmark and database snapshot from this repository (the dump in parts), or from the
# Hugging Face dataset when they are missing, verified against data/SHA256SUMS; the
# snapshot is restored read-only at build time.
ARG HF_DATASET={{DATASET_REPO}}
ARG HF_REVISION=main
RUN base="https://huggingface.co/datasets/${HF_DATASET}/resolve/${HF_REVISION}" \
 && for f in benchmark_500.json benchmark_500.csv benchmark_500.meta.json; do \
        [ -s "material/$f" ] || curl -fsSL -o "material/$f" "$base/$f"; done \
 && if ls data/snapshot.dump.part* >/dev/null 2>&1; then cat data/snapshot.dump.part* > data/snapshot.dump; \
    else curl -fsSL -o data/snapshot.dump "$base/snapshot.dump"; fi \
 && sha256sum -c data/SHA256SUMS \
 && initdb -D "$PGDATA" -U herikg --auth=trust -E UTF8 --locale=C >/dev/null \
 && pg_ctl -D "$PGDATA" -o "-k /tmp -c listen_addresses=''" -w start \
 && createdb -h /tmp -U herikg herikg_snapshot \
 && pg_restore -h /tmp -U herikg -d herikg_snapshot --no-owner --no-privileges -j 2 data/snapshot.dump \
 && psql -h /tmp -U herikg -d herikg_snapshot -c "ANALYZE" \
 && psql -h /tmp -U herikg -d postgres \
      -c "ALTER DATABASE herikg_snapshot SET default_transaction_read_only = on" \
      -c "ALTER DATABASE herikg_snapshot SET statement_timeout = '120s'" \
      -c "ALTER DATABASE herikg_snapshot SET timezone = 'UTC'" \
 && pg_ctl -D "$PGDATA" -w stop \
 && rm -f data/snapshot.dump data/snapshot.dump.part*

ENV HERIKG_LOG_DIR=/tmp/herikg/logs
EXPOSE 7860
ENTRYPOINT ["bash", "start.sh"]
CMD []
