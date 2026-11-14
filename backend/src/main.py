# COBECO Backend — Ponto de Entrada Principal (FastAPI)
# Clean Architecture: main.py apenas configura e roda a aplicação

from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.adapters.api import auth, catalogo, comparacao, exportacao, listas, perfil
from src.adapters.db.database import close_db, init_db
from src.config import settings

# ============================================================
# Structured Logging
# ============================================================
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(settings.LOG_LEVEL),
)

logger = structlog.get_logger()

# ============================================================
# Security Headers Middleware
# ============================================================
async def security_headers_middleware(request: Request, call_next):
    """Adiciona headers de segurança (CSP, HSTS, etc.)"""
    response = await call_next(request)

    # Content Security Policy
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self'"
    )

    # Security Headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

    # HSTS (apenas em produção com HTTPS)
    if not settings.DEBUG:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

    return response


# ============================================================
# Lifespan — Startup/Shutdown
# ============================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia ciclo de vida da aplicação"""
    logger.info("starting_application", app_name=settings.APP_NAME, version=settings.APP_VERSION)

    # Startup: Inicializa DB
    await init_db()
    logger.info("database_initialized")

    yield

    # Shutdown: Fecha conexões
    await close_db()
    logger.info("application_shutdown")


# ============================================================
# FastAPI Application
# ============================================================
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="MVP de Comparação de Preços para Listas de Compras",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
    lifespan=lifespan,
)

# CORS Middleware (apenas se configurado)
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

# Security Headers Middleware (deve ser adicionado antes do logging)
app.middleware("http")(security_headers_middleware)


# ============================================================
# Middleware — Request Logging & Error Handling
# ============================================================
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log estruturado de requisições"""
    import time
    start_time = time.perf_counter()

    logger.info(
        "request_started",
        method=request.method,
        url=str(request.url),
        client_ip=request.client.host if request.client else None,
    )

    try:
        response = await call_next(request)
        duration = time.perf_counter() - start_time

        logger.info(
            "request_completed",
            method=request.method,
            url=str(request.url),
            status_code=response.status_code,
            duration_ms=round(duration * 1000, 2),
        )
        return response
    except Exception as e:
        duration = time.perf_counter() - start_time
        logger.error(
            "request_failed",
            method=request.method,
            url=str(request.url),
            error=str(e),
            duration_ms=round(duration * 1000, 2),
        )
        raise


# ============================================================
# Exception Handlers
# ============================================================
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content={"detail": "Recurso não encontrado", "code": "NOT_FOUND"},
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    logger.error("internal_server_error", error=str(exc), path=str(request.url))
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor", "code": "INTERNAL_ERROR"},
    )


# ============================================================
# Health Check
# ============================================================
@app.get("/health", tags=["Health"])
async def health_check():
    """Endpoint de health check para Docker e load balancers"""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


# ============================================================
# API Routers — Inclusão das rotas por domínio
# ============================================================
# Prefixos sem /v1/ pois o proxy faz o versionamento
app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(listas.router, prefix="/listas", tags=["Listas"])
app.include_router(catalogo.router, prefix="/catalogo", tags=["Catálogo"])
app.include_router(comparacao.router, prefix="/comparacao", tags=["Comparação"])
app.include_router(exportacao.router, prefix="/export", tags=["Exportação"])
app.include_router(perfil.router, prefix="/perfil", tags=["Perfil"])


# ============================================================
# Root
# ============================================================
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": f"Bem-vindo ao {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs" if settings.DEBUG else "Desabilitado em produção",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
