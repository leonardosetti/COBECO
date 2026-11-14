#!/usr/bin/env python3
"""MCP stdio JSON-RPC — nexus-ledger. Local-only, sem rede, sem PII."""
import json
import sys
import yaml
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mcp_usage_log import log_usage

LEDGER = ".ai/agents/ledger.yaml"


def load_ledger():
    with open(LEDGER, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def save_ledger(data):
    with open(LEDGER, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def handle(req):
    method = req.get("method")
    params = req.get("params") or {}
    rid = req.get("id")
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": rid, "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "mcp-nexus-ledger", "version": "0.1.0"},
        }}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": [
            {"name": "ledger_read", "description": "Lê .ai/agents/ledger.yaml", "inputSchema": {"type": "object", "properties": {}}},
            {"name": "ledger_append", "description": "Anexa entrada estruturada ao ledger (schema Art. 4.10)", "inputSchema": {"type": "object", "properties": {"task_id": {"type": "string"}, "sender": {"type": "string"}, "receiver": {"type": "string"}, "action": {"type": "string"}, "status": {"type": "string"}, "exit_status": {"type": "integer"}, "notes": {"type": "string"}}, "required": ["task_id", "sender", "receiver", "action", "status", "exit_status", "notes"]}},
        ]}}
    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments") or {}
        try:
            if name == "ledger_read":
                text = yaml.safe_dump(load_ledger(), allow_unicode=True, sort_keys=False)
            elif name == "ledger_append":
                required = ("task_id", "sender", "receiver", "action", "status", "exit_status", "notes")
                missing = [k for k in required if k not in args or args[k] is None]
                if missing:
                    return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32602, "message": f"campos obrigatórios ausentes: {', '.join(missing)}"}}
                data = load_ledger()
                if not isinstance(data, list):
                    data = []
                data.append({
                    "task_id": args["task_id"],
                    "sender": args["sender"],
                    "receiver": args["receiver"],
                    "action": args["action"],
                    "status": args["status"],
                    "exit_status": int(args["exit_status"]),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "notes": args["notes"],
                })
                save_ledger(data)
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
        params = req.get("params") or {}
        resp = handle(req)
        ok = resp.get("error") is None
        tool = params.get("name") if req.get("method") == "tools/call" else None
        log_usage("mcp-nexus-ledger", req.get("method"), tool, ok,
                  resp.get("error", {}).get("message") if not ok else None)
        if resp is not None and req.get("id") is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
