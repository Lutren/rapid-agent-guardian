# Devpost Submission Draft

## Project Name

Agent Safety Gate for Real Work

## Tagline

A Gemini-powered agent that helps teams complete real tasks with evidence,
partner MCP context and human approval gates.

## Inspiration

AI agents are useful only when they can do work without hiding the evidence.
The project explores a practical question: can an agent complete a real
workflow while making every step inspectable before action?

## What It Does

The agent takes a real goal, such as preparing a repository release. It plans
the steps, queries a partner MCP server for project state, creates an
observation envelope, evaluates the risk and produces a handoff packet for
human review.

## How It Uses Google Cloud

Target implementation:

- Gemini for reasoning and plan generation.
- Google Cloud Agent Builder or ADK for orchestration.
- Cloud Run or Agent Builder hosting for the demo endpoint.
- Google Cloud logging/tracing for execution evidence.

## Partner MCP

Primary partner target: GitLab MCP.

The agent uses project state such as issues, merge requests and pipelines to
decide whether a release should move forward, require review or be blocked.

## What Makes It Different

The agent is designed around evidence and handoff, not just response quality.
It gives a decision and the next human action rather than silently executing
high-risk work.

## Built With

- Gemini
- Google Cloud Agent Builder or ADK
- Partner MCP
- Python
- SQLite-compatible evidence model in later iteration
- Public-safe readiness gate

## Public Safety Boundary

This submission does not include private prompts, private orchestration,
MEDIOEVO canon, RPG/TCG material, family data, secrets or absolute safety
claims.

## Current Readiness

The local repo candidate passes the public-safe readiness gate when
`python -m rapid_agent_guardian.readiness --out runtime\submission_readiness.json`
returns `LOCAL_PUBLIC_SAFE`. Cloud demo readiness remains blocked until Google
Cloud CLI/project/credits and the official partner MCP endpoint are configured.

The clean public export is staged locally with `python scripts\export_public_repo.py`.
The staged copy excludes `runtime/`, caches, secrets and the broader workspace.

The public repository can include a GitHub Sponsor button. Sponsorship supports
the open maintenance and demo layer only; it does not include private
orchestration, proprietary internals or guaranteed outcomes.

## Demo Video Outline

1. Show the user goal.
2. Show the planned steps.
3. Show partner MCP evidence.
4. Show observation envelope and gate decision.
5. Show human handoff.
6. Explain why the agent did not silently publish.
