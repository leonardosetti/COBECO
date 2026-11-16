#!/usr/bin/env python3
"""mcp_usage_log.py — Log leve de uso dos servidores MCP (JSONL, local, stdlib).

Registra uma linha por requisicao: timestamp, servidor, metodo, ferramenta,
sucesso/falha e erro (quando houver). Sem rede, sem inferencia, custo
proporcional ao volume de requisicoes (append em arquivo local).

Uso em cada servidor MCP:
    from mcp_usage_log import log_usage
    ...
    resp = handle(req)
    log_usage(server_name, method, tool_name, ok=..., error=...)
"""
import json
from datetime import datetime, timezone
from pathlib import Path

LOG = Path(".ai/agents/mcp_usage.jsonl")


def log_usage(server: str, method: str, tool: str | None, ok: bool,
              error: str | None = None) -> None:
    """Anexa uma entrada JSONL ao log de uso do MCP."""
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "server": server,
        "method": method,
        "tool": tool,
        "ok": ok,
        "error": error,
    }
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
