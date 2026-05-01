from __future__ import annotations

import json
import os
import urllib.request
from typing import Any


class PartnerMCPClient:
    """Tiny JSON-RPC client with a deterministic dry-run fallback."""

    def __init__(self, endpoint: str | None = None, auth_header: str | None = None):
        self.endpoint = endpoint or os.environ.get("PARTNER_MCP_ENDPOINT", "")
        self.auth_header = auth_header or os.environ.get("PARTNER_MCP_AUTH", "")

    def call_tool(self, tool_name: str, params: dict[str, Any]) -> dict[str, Any]:
        if not self.endpoint:
            return self._dry_run(tool_name, params)

        payload = {
            "jsonrpc": "2.0",
            "id": f"rapid-agent-{tool_name}",
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": params},
        }
        request = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers=self._headers(),
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read().decode("utf-8")
        return json.loads(body)

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.auth_header:
            headers["Authorization"] = self.auth_header
        return headers

    @staticmethod
    def _dry_run(tool_name: str, params: dict[str, Any]) -> dict[str, Any]:
        target = str(params.get("target") or "unknown")
        return {
            "dryRun": True,
            "partner": "gitlab",
            "tool": tool_name,
            "target": target,
            "result": {
                "openIssues": 2,
                "pipelineStatus": "passing",
                "releaseChecklist": ["license", "tests", "secret scan", "human approval"],
            },
        }
