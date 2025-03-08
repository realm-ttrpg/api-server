FROM python:3.12-alpine
EXPOSE 5000
WORKDIR /app
STOPSIGNAL SIGTERM
ENV ENV=/app/.profile

RUN <<-EOF
	apk add git tzdata
	pip install -U pip setuptools
	addgroup --gid 1000 rpgserver
	adduser --disabled-password --home /app --uid 1000 \
		--ingroup rpgserver rpgserver
	chown -R rpgserver:rpgserver /app
EOF

USER rpgserver
COPY pyproject.toml /app/
COPY config.toml /app/
COPY requirements /app/requirements
COPY realm_api /app/realm_api

RUN <<-EOF
	mkdir -p /app/data
	pip install --no-cache -Ue .
EOF

ENTRYPOINT [ "/usr/local/bin/python", "-m", "aethersprite.webapp" ]
