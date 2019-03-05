FROM mozilla/redash:latest

USER root
RUN apt-get update && apt-get install -y python3 python3-pip libecpg-dev
RUN pip uninstall -qy redash-stmo \
	&& pip3 install flit
RUN pip install pgsanity
USER redash

ENTRYPOINT ["/extension/bin/docker-entrypoint"]
