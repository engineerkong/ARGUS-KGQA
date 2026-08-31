FROM python:3.11-slim

WORKDIR /app
COPY scripts/ scripts/
COPY obda/schema.sql obda/schema.sql

RUN pip install --no-cache-dir requests rdflib "psycopg[binary]"

ENTRYPOINT ["python", "scripts/0c_ingest_governance_pg.py"]
