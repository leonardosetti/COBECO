#!/usr/bin/env bash
# Auto-adesão de ferramentas FOSS (sem auth/token de API) ao contexto Opencode do COBECO.
# Archlinux (pacman). Critérios: custo zero, sem autenticação, nativas/aplicáveis ao Opencode, alta adoção comunitária.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
NPM_GLOBAL="$HOME/.npm-global"
export PATH="$NPM_GLOBAL/bin:$PATH"

echo "==> [1/5] Dependências de sistema (pacman)"
sudo pacman -S --needed --noconfirm python sqlite ripgrep ffmpeg imagemagick nodejs npm curl ca-certificates 2>&1 | tail -3

echo "==> [2/5] Servidores MCP locais (npm global, sem npx remoto)"
npm config set prefix "$NPM_GLOBAL"
npm install -g --no-audit --no-fund --allow-scripts=better-sqlite3 \
  @modelcontextprotocol/server-filesystem \
  @modelcontextprotocol/server-memory \
  mcp-server-sqlite \
  sharp 2>&1 | tail -3

echo "==> [3/5] Embeddings locais Python (sem API)"
python3 -m pip install --quiet --disable-pip-version-warning --break-system-packages sentence-transformers 2>/dev/null || true

echo "==> [4/5] Habilitar graphify no .planning/config.json"
mkdir -p .planning
node -e '
  const fs=require("fs");
  const p=".planning/config.json";
  const c=fs.existsSync(p)?JSON.parse(fs.readFileSync(p,"utf8")):{};
  c.graphify={enabled:true,auto_update:(c.graphify&&c.graphify.auto_update)||false};
  fs.writeFileSync(p,JSON.stringify(c,null,2)+"\n");
'

echo "==> [5/5] Banco vetorial embarcado (SQLite)"
if command -v sqlite3 >/dev/null 2>&1; then
  sqlite3 .planning/vector.db "CREATE TABLE IF NOT EXISTS chunks(rowid INTEGER PRIMARY KEY, content TEXT);" 2>/dev/null || true
fi

echo "OK: adesão concluída. Veja .opencode/mcp.json e .planning/config.json"
