#!/bin/bash
# COBECO MVP — Deploy Staging (Homologação)
# Porta: 8480 (evita conflito com dev 8380)
# Uso: ./scripts/deploy-stage.sh

set -euo pipefail

PROJECT_ROOT="/lab/FATEC/202602/lab_eng_software/COBECO"
STAGE_PORT=8480
STAGE_BRANCH="staging/$(date +%Y%m%d-%H%M%S)"

cd "$PROJECT_ROOT"

echo "🚀 Iniciando deploy de staging..."
echo "   Branch: $STAGE_BRANCH"
echo "   Porta: $STAGE_PORT"

# 1. Verifica se há mudanças não commitadas
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "⚠️  Há mudanças não commitadas. Commit ou stash antes de continuar."
    exit 1
fi

# 2. Atualiza main
echo "📥 Atualizando main..."
git checkout main
git pull origin main

# 3. Cria branch de staging
echo "🌿 Criando branch $STAGE_BRANCH..."
git checkout -b "$STAGE_BRANCH"

# 4. Merge de todos os PRs com fixes
echo "🔀 Fazendo merge dos fixes..."
for branch in \
    "fix/bug-001-user-registration" \
    "fix/bug-007-irrelevant-products" \
    "fix/bug-003-search-focus" \
    "fix/bug-006-large-areas" \
    "fix/bug-002-save-list-modal"
do
    echo "   Merging $branch..."
    bug_num=$(echo "$branch" | sed -E 's/fix\/bug-([0-9]+).*/\1/')
    git merge "origin/$branch" --no-ff -m "fix: BUG-$bug_num - merge $branch into staging" || {
        echo "❌ Conflito ao mergear $branch. Resolva manualmente."
        exit 1
    }
done

# 5. Push da branch de staging
echo "📤 Push da branch de staging..."
git push origin "$STAGE_BRANCH" --no-verify

# 6. Sobe ambiente de staging
echo "🐳 Subindo ambiente de staging (porta $STAGE_PORT)..."
docker compose -f docker-compose.stage.yml down -v 2>/dev/null || true
docker compose -f docker-compose.stage.yml build --no-cache
docker compose -f docker-compose.stage.yml up -d

# 6. Aguarda healthchecks
echo "⏳ Aguardando serviços ficarem saudáveis..."
sleep 10

# 7. Verifica saúde dos containers
echo "🔍 Verificando saúde..."
for i in {1..30}; do
    if curl -sf "http://localhost:$STAGE_PORT/" >/dev/null 2>&1; then
        echo "✅ Frontend respondendo em http://localhost:$STAGE_PORT"
        break
    fi
    sleep 2
    if [ $i -eq 30 ]; then
        echo "❌ Timeout aguardando frontend"
        docker compose -f docker-compose.stage.yml logs --tail=50
        exit 1
    fi
done

# 8. Executa migrações do banco
echo "🗄️ Executando migrações do banco de dados..."
docker exec cobeco-backend-stage alembic -c config-alembic-0001-alembic-v1.0.ini upgrade head

# 9. Popula banco com seed data
echo "🌱 Populando banco com seed data..."
docker exec cobeco-backend-stage python scripts/script-seed-0005-generate-realistic-seed.py --profile realistico | docker exec -i cobeco-db-stage mysql -u cobeco -pcobeco cobeco_stage

# 10. Verifica API backend
for i in {1..30}; do
    if curl -sf "http://localhost:$STAGE_PORT/v1/catalogo/categorias" >/dev/null 2>&1; then
        echo "✅ Backend API respondendo"
        break
    fi
    sleep 2
    if [ $i -eq 30 ]; then
        echo "❌ Timeout aguardando backend API"
        docker compose -f docker-compose.stage.yml logs --tail=50 backend
        exit 1
    fi
done

# 11. Roda testes de smoke
echo "🧪 Rodando testes de smoke..."
if command -v pytest >/dev/null 2>&1; then
    pytest tests/integration/ -v --tb=short -x -k "stage or smoke" 2>&1 | head -50
fi

echo ""
echo "✅ Staging deployado com sucesso!"
echo "   URL: http://localhost:$STAGE_PORT"
echo "   Branch: $STAGE_BRANCH"
echo "   Para ver logs: docker compose -f docker-compose.stage.yml logs -f"
echo "   Para parar: docker compose -f docker-compose.stage.yml down -v"
echo ""
echo "📋 PRs incluídos:"
echo "   #90 - BUG-001: Cadastro com auto-login"
echo "   #91 - BUG-007: Filtra produtos irrelevantes"
echo "   #92 - BUG-003: Campo busca perde foco"
echo "   #93 - BUG-006: Mapeamento grandes áreas"
echo "   #94 - BUG-002: Fluxo salvar lista modal"
