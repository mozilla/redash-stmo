FROM mozilla/redash:latest

ENV PYTHONUNBUFFERED=0 \
	PYTHONPATH=/redash-stmo:/redash-stmo/src:/app \
	REDASH_LOG_LEVEL="INFO" \
	REDASH_REDIS_URL=redis://redis:6379/0 \
	REDASH_DATABASE_URL=postgresql://postgres@postgres/postgres

USER root
RUN pip uninstall -y redash-stmo
USER redash

ENTRYPOINT ["/redash-stmo/bin/docker-entrypoint"]
