from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_id(prefix: str, data: dict[str, Any]) -> str:
    payload = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return f"{prefix}_{hashlib.sha256(payload.encode('utf-8')).hexdigest()[:16]}"


@dataclass
class GoalRequest:
    goal: str
    actor: str
    target: str
    partner: str
    risk: float = 0.5
    reversibility: float = 0.5
    human_review: bool = False
    requested_actions: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GoalRequest":
        return cls(
            goal=str(data.get("goal") or ""),
            actor=str(data.get("actor") or "agent"),
            target=str(data.get("target") or ""),
            partner=str(data.get("partner") or "gitlab"),
            risk=float(data.get("risk", 0.5)),
            reversibility=float(data.get("reversibility", 0.5)),
            human_review=bool(data.get("human_review") or data.get("humanReview")),
            requested_actions=[str(item) for item in data.get("requested_actions", []) if item],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "goal": self.goal,
            "actor": self.actor,
            "target": self.target,
            "partner": self.partner,
            "risk": self.risk,
            "reversibility": self.reversibility,
            "humanReview": self.human_review,
            "requestedActions": self.requested_actions,
        }


@dataclass
class ObservationEnvelope:
    observer: str
    subject: str
    claim: str
    evidence: list[dict[str, Any]]
    observed_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        data = {
            "observer": self.observer,
            "subject": self.subject,
            "claim": self.claim,
            "evidence": self.evidence,
            "observedAt": self.observed_at,
        }
        return {
            "schemaVersion": "rapid_agent_guardian.observation_envelope.v1",
            "id": stable_id("obs", data),
            **data,
        }


@dataclass
class GateDecision:
    status: str
    reasons: list[str]
    score: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemaVersion": "rapid_agent_guardian.gate_decision.v1",
            "status": self.status,
            "score": round(self.score, 3),
            "reasons": self.reasons,
        }
