#!/usr/bin/env python3
"""MCP stdio JSON-RPC — nexus-dispatch. Local-only, sem rede, sem PII."""
import json
import sys
import yaml
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mcp_usage_log import log_usage

REGISTRY = ".ai/agents/registry.yaml"


def load_registry():
    with open(REGISTRY, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def handle(req):
    method = req.get("method")
    params = req.get("params") or {}
    rid = req.get("id")
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": rid, "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "mcp-nexus-dispatch", "version": "0.1.0"},
        }}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": [
            {"name": "dispatch_registry_read", "description": "Lê .ai/agents/registry.yaml", "inputSchema": {"type": "object", "properties": {}}},
            {"name": "dispatch_validate", "description": "Valida estrutura do registry de agentes", "inputSchema": {"type": "object", "properties": {}}},
        ]}}
    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments") or {}
        try:
            if name == "dispatch_registry_read":
                text = yaml.safe_dump(load_registry(), allow_unicode=True, sort_keys=False)
            elif name == "dispatch_validate":
                reg = load_registry()
                agents = reg.get("agents") if isinstance(reg, dict) else None
                ok = isinstance(agents, list) and len(agents) > 0
                text = "valido" if ok else "invalido: agentes ausentes"
                return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": text}, {"type": "text", "text": f"agents={len(agents) if agents else 0}"}]}}
            else:
                return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "tool desconhecida"}}
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": text}]}}
        except Exception as exc:  # noqa: BLE001
            return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32603, "message": str(exc)}}
    return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "método desconhecido"}}


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        resp = handle(req)
        params = req.get("params") or {}
        ok = resp.get("error") is None
        tool = params.get("name") if req.get("method") == "tools/call" else None
        log_usage("mcp-nexus-dispatch", req.get("method"), tool, ok,
                  resp.get("error", {}).get("message") if not ok else None)
        if resp is not None and req.get("id") is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
