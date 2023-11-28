FROM --platform=linux/amd64 python:3.11-slim-buster AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_ROOT_USER_ACTION=ignore

WORKDIR /app
COPY requirements.txt src /app/
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
