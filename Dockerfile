FROM mozilla/redash:latest

USER root
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip uninstall -qy redash-stmo \
	&& pip3 install flit
USER redash

ENTRYPOINT ["/extension/bin/docker-entrypoint"]
