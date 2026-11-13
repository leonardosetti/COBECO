# COBECO Backend — Perfil Router (FastAPI)
# Endpoints já cobertos em auth.py (/auth/perfil, /auth/perfil PUT)
# Este arquivo mantém a estrutura modular

from fastapi import APIRouter

router = APIRouter(tags=["Perfil"])

# Endpoints de perfil estão em auth.py:
# GET  /v1/auth/perfil      -> Visualizar Perfil (UC18/RF05)
# PUT  /v1/auth/perfil      -> Gerenciar Perfil (UC16/RF06)

# Este router existe para manter a estrutura modular da Clean Architecture
# e pode ser expandido com endpoints específicos de perfil no futuro

@router.get("/health")
async def perfil_health():
    return {"status": "ok", "module": "perfil"}