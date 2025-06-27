# Stage 1: Builder
FROM python:3.9-slim-buster AS builder
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /usr/src/app/wheels -r requirements.txt

# Stage 2: Final Image
FROM python:3.9-slim-buster
WORKDIR /usr/src/app
RUN addgroup --system app && adduser --system --group app
COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --no-cache /wheels/*
COPY ./app ./app
RUN chown -R app:app /usr/src/app
USER app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]