#!/usr/bin/env python3
"""MCP stdio JSON-RPC — nexus-kb. Local-only, sem rede, sem PII."""
import json
import sys
import os
import yaml
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mcp_usage_log import log_usage

KB = ".ai/knowledge_base.yaml"


def load_kb():
    if not os.path.exists(KB):
        return {}
    with open(KB, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def save_kb(data):
    with open(KB, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def handle(req):
    method = req.get("method")
    params = req.get("params") or {}
    rid = req.get("id")
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": rid, "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "mcp-nexus-kb", "version": "0.1.0"},
        }}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": [
            {"name": "kb_read", "description": "Lê a base de conhecimento local .ai/knowledge_base.yaml", "inputSchema": {"type": "object", "properties": {}}},
            {"name": "kb_append", "description": "Anexa entrada de grafo de conhecimento à KB", "inputSchema": {"type": "object", "properties": {"key": {"type": "string"}, "value": {"type": "string"}}, "required": ["key", "value"]}},
        ]}}
    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments") or {}
        try:
            if name == "kb_read":
                text = yaml.safe_dump(load_kb(), allow_unicode=True, sort_keys=False)
            elif name == "kb_append":
                data = load_kb()
                data[args.get("key", "")] = args.get("value", "")
                save_kb(data)
                text = "ok"
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
        log_usage("mcp-nexus-kb", req.get("method"), tool, ok,
                  resp.get("error", {}).get("message") if not ok else None)
        if resp is not None and req.get("id") is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
