FROM redash/redash:latest

COPY . /redash-stmo

ENV PYTHONUNBUFFERED=0 \
	PYTHONPATH=/app/ \
	REDASH_LOG_LEVEL="INFO" \
	REDASH_REDIS_URL=redis://redis:6379/0 \
	REDASH_DATABASE_URL=postgresql://postgres@postgres/postgres

USER root
RUN pip install -e /redash-stmo
USER redash

ENTRYPOINT ["/redash-stmo/bin/docker-entrypoint"]
