# Agent Safety Gate for Real Work

Google Cloud Rapid Agent Hackathon prep package.

## Positioning

[Sponsor the work](https://github.com/sponsors/Lutren)

Sponsor goal: 25 monthly sponsors to fund public-safe docs, tests, release checklists, sanitized examples, and lightweight demos for local-first AI agent safety gates.

Suggested monthly tiers: $5 Observer, $19 Builder, $50 Lab, $100 Patron, and $500 Integration Sponsor. Sponsorship supports the open layer; private orchestration, private prompts, unreleased canon, RPG/TCG material, secrets, and implementation internals stay out of the public package.

This project is a public-safe hackathon candidate for the Google Cloud Rapid
Agent Hackathon. It demonstrates an agent that goes beyond chat by planning a
multi-step release or operations task, gathering evidence from a partner MCP
surface, producing an audit envelope, and deciding whether the action should be
approved, reviewed, or blocked.

The open demo does not include private prompts, private orchestration, MEDIOEVO
canon, RPG/TCG data, family data, secrets, or paid implementation internals.

## Default Submission Idea

**Agent Safety Gate for Real Work**: a Gemini-powered agent that helps builders
ship changes safely. The user gives it a goal such as "prepare this repo for a
release". The agent:

1. plans concrete steps;
2. asks a partner MCP server for project state;
3. records evidence and provenance;
4. runs a review gate;
5. produces a handoff packet for human approval.

Initial partner target: GitLab MCP, because it naturally maps to issues, merge
requests, pipelines and release workflows.

## Local Demo

```powershell
cd "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\hackathons\google-rapid-agent-2026"
python -m rapid_agent_guardian.cli examples\release_goal.json --out runtime\demo_packet.json
python -m rapid_agent_guardian.readiness --out runtime\submission_readiness.json
python scripts\export_public_repo.py
python -m unittest discover -s tests
```

## Cloud Path

The hackathon page requires a functional agent powered by Gemini and Google
Cloud Agent Builder, plus a participating partner MCP integration. This package
is the local, public-safe foundation. When credits and final partner details are
available, deploy the same flow through Agent Builder or ADK on Google Cloud.

## Status

- Local scaffold: ready.
- Cloud environment: blocked until Google Cloud CLI / project / credits are set.
- Partner MCP: dry-run interface ready; real endpoint waits for the official
  partner resource details.
- Publication gate: `rapid_agent_guardian.readiness` verifies the public export
  set and keeps cloud demo readiness blocked until `gcloud` and a real partner
  MCP endpoint are configured.
- Public export: `scripts/export_public_repo.py` stages only allowlisted files
  into `publish_staging/hackathons/google-rapid-agent-2026-public-safe`.
- Funding metadata: `.github/FUNDING.yml` points to `Lutren` so GitHub can show
  the Sponsor button.
- Submission: draft only, not published.
