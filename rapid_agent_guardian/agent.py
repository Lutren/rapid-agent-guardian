from __future__ import annotations

from typing import Any

from .mcp_client import PartnerMCPClient
from .models import GateDecision, GoalRequest, ObservationEnvelope, utc_now


def plan_steps(goal: GoalRequest) -> list[str]:
    requested = goal.requested_actions or ["inspect_project", "collect_evidence", "draft_handoff"]
    steps = ["parse_goal"]
    steps.extend(requested)
    steps.append("evaluate_gate")
    steps.append("produce_handoff_packet")
    return steps


def evaluate_gate(goal: GoalRequest, evidence: list[dict[str, Any]]) -> GateDecision:
    reasons: list[str] = []
    verified_count = sum(1 for item in evidence if item.get("verified"))
    evidence_score = min(1.0, verified_count / max(1, len(evidence)))
    risk_pressure = max(0.0, goal.risk - goal.reversibility)
    score = max(0.0, min(1.0, 0.65 * evidence_score + 0.35 * goal.reversibility - risk_pressure))

    if verified_count == 0:
        reasons.append("no verified partner evidence")
    if goal.risk >= 0.8 and not goal.human_review:
        reasons.append("high risk action requires human review")
    if not goal.human_review:
        reasons.append("human review missing")

    if score < 0.7 and not reasons:
        reasons.append("score below approval band")

    if any("high risk" in reason for reason in reasons):
        status = "BLOCK"
    elif reasons or score < 0.7:
        status = "REVIEW"
    else:
        status = "APPROVE"
        reasons.append("verified evidence and human review satisfy release gate")

    return GateDecision(status=status, reasons=reasons, score=score)


def build_handoff_packet(goal: GoalRequest, mcp_client: PartnerMCPClient | None = None) -> dict[str, Any]:
    client = mcp_client or PartnerMCPClient()
    steps = plan_steps(goal)
    partner_result = client.call_tool(
        "project_status",
        {"target": goal.target, "requestedActions": goal.requested_actions},
    )
    evidence = [
        {
            "id": "partner_project_status",
            "label": "Partner MCP project status",
            "source": goal.partner,
            "verified": not bool(partner_result.get("dryRun")),
            "summary": partner_result.get("result", partner_result),
        },
        {
            "id": "human_review_flag",
            "label": "Human review flag",
            "source": "goal_request",
            "verified": goal.human_review,
            "summary": {"humanReview": goal.human_review},
        },
    ]
    envelope = ObservationEnvelope(
        observer=goal.actor,
        subject=goal.target,
        claim=f"Agent prepared a gated plan for: {goal.goal}",
        evidence=evidence,
    )
    decision = evaluate_gate(goal, evidence)
    return {
        "schemaVersion": "rapid_agent_guardian.handoff_packet.v1",
        "createdAt": utc_now(),
        "goal": goal.to_dict(),
        "steps": steps,
        "partnerMcp": partner_result,
        "observationEnvelope": envelope.to_dict(),
        "gateDecision": decision.to_dict(),
        "nextHumanAction": "review_and_approve" if decision.status != "BLOCK" else "revise_goal_or_reduce_risk",
        "claims": {
            "agentAutonomy": "human_supervised",
            "thresholds": "demo_only",
            "privateIp": "not_included",
        },
    }
