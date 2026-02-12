# ---- Base image ----
FROM python:3.13-slim

# ---- System settings ----
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---- Workdir ----
WORKDIR /app

# ---- Install system deps (если потребуется requests + ssl) ----
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---- Install Python deps ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy project ----
COPY ./app ./app
COPY app/.env .env

# ---- Create directory for generated files ----
RUN mkdir -p /app/files

# ---- Expose port ----
EXPOSE 8082

# ---- Run FastAPI ----
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8082"]
