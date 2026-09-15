from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Callable
from urllib.request import Request, urlopen

Json = dict[str, Any]
Transport = Callable[[str, str, Json | None], Json]


def _http_transport(base_url: str) -> Transport:
    base = base_url.rstrip('/')
    def call(method: str, path: str, body: Json | None = None) -> Json:
        data = None if body is None else json.dumps(body).encode('utf-8')
        req = Request(base + path, data=data, method=method, headers={'Content-Type': 'application/json'})
        with urlopen(req, timeout=10) as response:  # nosec - operator-configured local EVO endpoint
            return json.loads(response.read().decode('utf-8'))
    return call


@dataclass
class LiveEvoAdapter:
    """Thin transport adapter. EVO remains owner of facts, auth and Command execution."""
    base_url: str = 'http://127.0.0.1:3000'
    transport: Transport | None = None

    def __post_init__(self) -> None:
        if self.transport is None:
            self.transport = _http_transport(self.base_url)

    def observation(self) -> Json:
        assert self.transport is not None
        return self.transport('GET', '/api/v1/apm/observation', None)

    def admit_command_proposal(self, proposal: Json) -> Json:
        assert self.transport is not None
        result = self.transport('POST', '/api/v1/apm/command-proposals/admit', proposal)
        if result.get('executionStatus') != 'NOT_EXECUTED':
            raise RuntimeError('EVO proposal admission crossed the execution boundary')
        return result

    def execute_action(self, action_request: Json) -> Json:
        assert self.transport is not None
        return self.transport('POST', '/api/v1/apm/actions/execute', action_request)
