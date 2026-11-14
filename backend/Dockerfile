# COBECO Backend — FastAPI + Python 3.11
# Multi-stage build para produção

# ============================================================
# BASE — Dependências de sistema e Python
# ============================================================
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Dependências de sistema para MySQL client e build
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    default-mysql-client \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# ============================================================
# RUNTIME — Imagem final com dependências
# ============================================================
FROM base AS runtime

COPY requirements.txt .
RUN pip install --no-warn-script-location -r requirements.txt
ENV PATH=/usr/local/bin:$PATH

# Copia código da aplicação
COPY . .

# Usuário não-root para segurança
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]