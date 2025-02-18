FROM python:3.12-slim

WORKDIR /usr/src/app/server
COPY ./docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN adduser --system --shell /bin/bash --home /home/nonroot nonroot && mkdir -p /usr/src/app/server && chown nonroot -R /usr/src/app && \
    pip install --no-cache-dir --upgrade poetry wheel pysu && \
    chmod +rx /usr/local/bin/docker-entrypoint.sh && apt update && apt install nmap openssh-client sshpass ipmitool -y

USER nonroot

COPY ./pyproject.toml ./poetry.lock ./

RUN poetry install --no-cache --no-root --with dev --with postgres

USER root
EXPOSE 8000
ENTRYPOINT [ "/usr/local/bin/docker-entrypoint.sh" ]
CMD poetry run aerich upgrade && poetry run uvicorn --host 0.0.0.0 --port 8000 --reload marron_machine:app