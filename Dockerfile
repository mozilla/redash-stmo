FROM redash/redash:latest
COPY . ./extensions
ENTRYPOINT ["/app/bin/docker-entrypoint"]