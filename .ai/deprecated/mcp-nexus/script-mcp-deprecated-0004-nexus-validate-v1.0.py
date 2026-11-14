#!/usr/bin/env python3
"""MCP stdio JSON-RPC — nexus-validate. Local-only, sem rede, sem PII."""
import json
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mcp_usage_log import log_usage

SCRIPTS = "scripts"


def handle(req):
    method = req.get("method")
    params = req.get("params") or {}
    rid = req.get("id")
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": rid, "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "mcp-nexus-validate", "version": "0.1.0"},
        }}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": [
            {"name": "validate_mcp", "description": "Valida sintaxe dos servidores scripts/mcp_*.py", "inputSchema": {"type": "object", "properties": {}}},
        ]}}
    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments") or {}
        try:
            if name == "validate_mcp":
                files = sorted(f for f in os.listdir(SCRIPTS) if f.startswith("mcp_") and f.endswith(".py"))
                report = []
                for f in files:
                    path = os.path.join(SCRIPTS, f)
                    try:
                        with open(path, "r", encoding="utf-8") as fh:
                            compile(fh.read(), path, "exec")
                        report.append(f"OK {f}")
                    except Exception as exc:  # noqa: BLE001
                        report.append(f"FALHA {f}: {exc}")
                text = "\n".join(report) if report else "nenhum servidor mcp_ encontrado"
                return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": text}]}}
            else:
                return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "tool desconhecida"}}
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
        log_usage("mcp-nexus-validate", req.get("method"), tool, ok,
                  resp.get("error", {}).get("message") if not ok else None)
        if resp is not None and req.get("id") is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
