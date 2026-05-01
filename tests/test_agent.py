from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from rapid_agent_guardian import GoalRequest, build_handoff_packet
from rapid_agent_guardian.readiness import check_submission_readiness
from scripts.export_public_repo import export_public_repo


class RapidAgentGuardianTests(unittest.TestCase):
    def test_builds_review_packet_with_dry_run_partner(self) -> None:
        goal = GoalRequest(
            goal="Prepare release handoff",
            actor="test-agent",
            target="demo/repo",
            partner="gitlab",
            risk=0.6,
            reversibility=0.8,
            human_review=True,
            requested_actions=["inspect_open_issues"],
        )
        packet = build_handoff_packet(goal)
        self.assertEqual(packet["schemaVersion"], "rapid_agent_guardian.handoff_packet.v1")
        self.assertEqual(packet["partnerMcp"]["partner"], "gitlab")
        self.assertEqual(packet["gateDecision"]["status"], "REVIEW")
        self.assertIn("observationEnvelope", packet)

    def test_blocks_high_risk_without_review(self) -> None:
        goal = GoalRequest(
            goal="Publish production release",
            actor="test-agent",
            target="demo/repo",
            partner="gitlab",
            risk=0.9,
            reversibility=0.2,
            human_review=False,
        )
        packet = build_handoff_packet(goal)
        self.assertEqual(packet["gateDecision"]["status"], "BLOCK")
        self.assertIn("high risk action requires human review", packet["gateDecision"]["reasons"])

    def test_submission_readiness_is_local_public_candidate(self) -> None:
        report = check_submission_readiness(".")
        self.assertEqual(report["decision"], "LOCAL_PUBLIC_SAFE")
        self.assertTrue(report["localPublicationCandidate"])
        self.assertFalse(report["cloudDemoReady"])
        self.assertIn("real partner MCP endpoint not configured", report["cloudBlockers"])

    def test_public_export_excludes_runtime(self) -> None:
        with TemporaryDirectory() as tmp:
            out = Path(tmp) / "public-export"
            manifest = export_public_repo(".", out)
            self.assertEqual(manifest["decision"], "PUBLIC_EXPORT_STAGED")
            self.assertTrue((out / "README.md").exists())
            self.assertTrue((out / "PUBLIC_EXPORT_MANIFEST.json").exists())
            self.assertFalse((out / "runtime").exists())


if __name__ == "__main__":
    unittest.main()
