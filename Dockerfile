FROM python:3.12.9-alpine3.21 AS base


# Basic env vars
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Create rootless user for running app
RUN addgroup --system app_group \
    && adduser --system --home /app --gecos "Rootless user for managing bot." \
        --disabled-password --ingroup app_group app_user

# Installing python dependencies via poetry
FROM base AS builder

ENV POETRY_VERSION=2.1.1

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

COPY ./pyproject.toml /app
RUN poetry config virtualenvs.in-project true && \
    poetry install --only=main --no-cache --no-interaction --no-ansi


# Copying other files and running app under rootless user
FROM base AS final

COPY --from=builder --chown=root:root --chmod=755 /app/.venv /app/.venv
COPY --chown=root:root --chmod=755 . /app

USER app_user

CMD [ "/app/.venv/bin/python3", "main.py" ]
