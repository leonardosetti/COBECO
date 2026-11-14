# Ferramentas aderidas — SpecDrivenDev / AI-Driven dev (COBECO)

Critério de aceite: custo zero (FOSS), sem autenticação/token de API, nativas ou aplicáveis ao Opencode, alta adoção comunitária.

## 1. MCP servers (Model Context Protocol) — rodam localmente, sem auth

| Servidor | Pacote | Uso | Auth |
|----------|--------|-----|------|
| filesystem | `@modelcontextprotocol/server-filesystem` | Leitura/escrita de arquivos do repositório | não |
| git | `@modelcontextprotocol/server-git` | Operações git (branches, diff, log, commits) | não |
| memory | `@modelcontextprotocol/server-memory` | Memória/KG local para contexto entre sessões | não |
| fetch | `mcp-server-fetch` | Requisições HTTP a páginas públicas (busca web sem API key) | não |
| sqlite | `mcp-server-sqlite` + extensão `vec0` | Banco vetorial embarcado (análise semântica local) | não |

Config: `.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/mcp.json`

## 2. Análise semântica e banco vetorial (local, sem API)

| Ferramenta | Pacote | Uso |
|------------|--------|-----|
| tree-sitter | `tree-sitter` + grammars | Parsing semântico de código (AST) |
| ripgrep | `ripgrep` | Busca textual rápida sobre o código |
| sentence-transformers | `sentence-transformers` (Python) | Embeddings locais para busca semântica |
| SQLite + vec0 | `mcp-server-sqlite` + `vec0` | Índice vetorial embarcado em `.planning/vector.db` |

## 3. Economia de tokens

| Ferramenta | Uso |
|------------|-----|
| `tiktoken` | Contagem exata de tokens por modelo |
| `workflow.compact_content` (GSD) | Instruções minimizadas (já em settings) |
| `graphify.auto_update` | Grafo recriado apenas quando necessário |

## 4. Webcrawler / busca otimizada na web (páginas públicas, sem API)

| Ferramenta | Uso |
|------------|-----|
| `mcp-server-fetch` | Fetch de páginas web públicas via MCP |
| `playwright` / `cheerio` + `axios` | Scraping local de páginas públicas (sem API key) |

> Limite: motores de busca (Google/Brave) exigem API key. O crawler aqui busca apenas páginas públicas diretamente informadas.

## 5. Manipulador de dados e imagens (local, FOSS)

| Ferramenta | Pacote | Uso |
|------------|--------|-----|
| sharp | `sharp` (Node) | Redimensionar, converter, metadados de imagem |
| pillow | `Pillow` (Python) | Processamento de imagem |
| polars / pandas | `polars`, `pandas` (Python) | Manipulação de dados tabulares |
| ffmpeg | `ffmpeg` | Áudio/vídeo (extração de frames, transcodificação) |

## 6. Graphify (knowledge graph do projeto)

Já presente via `@opengsd/gsd-core`. Habilitado em `.planning/config-planning-0001-planning-config-v1-planning-0001-planning-config-v1.0-planning-0001-planning-config-v1.0-planning-0001-planning-config-v1.0.json`:

```json
{ "graphify": { "enabled": true, "auto_update": false } }
```

Comando: `/gsd-graphify build`

## Instalação automática

Executar:

```bash
chmod +x scripts/script-tools-0001-auto-adesao-tools-v1.0.sh
./scripts/script-tools-0001-auto-adesao-tools-v1.0.sh
```

Instala dependências de sistema, pacotes Node/Python, habilita graphify e cria o banco vetorial embarcado.
