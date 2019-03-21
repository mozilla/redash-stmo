FROM mozilla/redash:latest

USER root
RUN apt-get update && apt-get install -y python3 python3-pip libecpg-dev
RUN pip uninstall -qy redash-stmo \
	&& pip3 install flit
RUN mkdir -p /home/redash/.cache /home/redash/.local /app/node_modules && \
	chown -R redash /home/redash/.cache /home/redash/.local /app/node_modules
USER redash

ENTRYPOINT ["/extension/bin/docker-entrypoint"]
