FROM python:3.11

WORKDIR /app

ENV PATH="/root/.local/bin:${PATH}"
ENV PYTHONBUFFERED=0 \
    POETRY_VIRTUALENVS_CREATE=false


ARG POETRY_VERSION
ENV POETRY_VERSION="${POETRY_VERSION:-1.1.14}"
RUN curl -sSL https://install.python-poetry.org \
  | python3 - --git https://github.com/python-poetry/poetry.git#{$POETRY_VERSION} \
 && poetry --version


COPY poetry.lock pyproject.toml ./
COPY app ./app

RUN poetry install
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
