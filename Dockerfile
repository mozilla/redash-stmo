FROM mozilla/redash:rc

ENV PATH="/home/redash/.local/bin:$PATH" \
	PYTHONUNBUFFERED=0 \
    REDASH_HOST="localhost:5000"


USER root
RUN apt-get update -yq \
    && apt-get install curl gnupg libecpg-dev -yq \
    && curl -sL https://deb.nodesource.com/setup_10.x | bash \
    && apt-get install nodejs -yq
RUN pip uninstall -qy redash-stmo \
	&& pip install -U pip virtualenv
RUN mkdir -p /home/redash/.cache /home/redash/.local /app/node_modules && \
	chown -R redash /home/redash/.cache /home/redash/.local /app/node_modules

COPY . /extension
RUN chown -R redash /extension
USER redash

ENTRYPOINT ["/extension/bin/docker-entrypoint"]
