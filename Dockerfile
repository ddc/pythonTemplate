FROM python:3.12-slim-bookworm AS python-base

LABEL Description="App"

ENV TERM=xterm \
    TZ="UTC" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_ROOT_USER_ACTION=ignore \
    POETRY_HOME="/opt/poetry" \
    POETRY_VERSION=1.8.3 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH=/opt/poetry/bin:$PATH

WORKDIR /opt/app
RUN mkdir -p /opt/app/logs

RUN set -ex \
    && apt-get update \
    && apt-get install --no-install-recommends -y curl \
    && curl -sSL https://install.python-poetry.org | python3 - --version "$POETRY_VERSION" \
    && apt-get autoremove -y \
    && apt-get clean

RUN useradd -ms /bin/bash app

COPY --chown=app:app pyproject.toml poetry.lock .env /opt/app/
RUN poetry install --no-interaction --no-ansi --sync $(if [ "$CONFIG_ENV" = 'prod' ]; then echo '--only main'; fi)

USER app
CMD ["python", "main.py"]
