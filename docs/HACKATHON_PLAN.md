# Google Cloud Rapid Agent Hackathon Plan

Date: 2026-05-01

## Verified Facts

- Devpost page: `https://rapid-agent.devpost.com/`
- Schedule: May 5 to Jun 11, 2026.
- Prize pool: 60,000 USD.
- Submissions open soon.
- Requirement: build a functional agent powered by Gemini and Google Cloud Agent Builder.
- Requirement: integrate a participating partner's MCP server.
- Submission requires a hosted project URL, public open-source code repository, approximately 3 minute demo video, challenge selection and Devpost form.
- Current listed partner prize tracks include Elastic, Arize, Dynatrace, GitLab, MongoDB and Fivetran.

## Chosen Idea

Agent Safety Gate for Real Work.

The agent helps builders complete a release or operations workflow. It plans
steps, asks a partner MCP server for project state, creates an evidence packet,
runs a gate and produces a human handoff.

## Why This Fits

- It is not a chatbot: it creates a handoff packet and gate decision.
- It handles multi-step work: inspect, collect evidence, evaluate, hand off.
- It keeps the human in control.
- It uses a partner MCP path: GitLab MCP first, with optional Arize or Dynatrace
  observability later.
- It supports the user's thesis without exposing private implementation.

## Public Boundary

Public:

- generic safety gate logic;
- handoff packet schema;
- dry-run MCP client;
- demo release workflow;
- MIT license.

Private or paid:

- internal prompts;
- full Claudio/Brain OS orchestration;
- MEDIOEVO canon;
- RPG/TCG material;
- family data;
- customer-specific integrations;
- advanced evaluation harnesses.

## Build Milestones

1. Local scaffold and tests.
2. Local readiness gate for public-safe repo extraction.
3. Public repo extraction from allowlist only.
4. Google Cloud project setup after credits are announced.
5. Agent Builder or ADK implementation with Gemini.
6. Partner MCP integration, starting with GitLab.
7. Cloud Run or Agent Builder hosted demo.
8. Three minute demo video script and capture.
9. Devpost submission.

## Cloud Setup Checklist

- Install Google Cloud CLI.
- Create or select a Google Cloud project.
- Apply for hackathon credits when the link is announced.
- Enable billing only after credits are attached.
- Enable Vertex AI / Agent Builder APIs.
- Decide region.
- Create a service account with minimum permissions.
- Do not upload local secrets, private canon, RPG/TCG files or workspace-wide zips.
- Run `python -m rapid_agent_guardian.readiness --out runtime\submission_readiness.json`
  before extracting the public repo.
- Run `python scripts\export_public_repo.py` to stage the clean public-safe repo
  locally before any GitHub publication.

## Funding Boundary

The public repo may include `.github/FUNDING.yml` with `github: Lutren` so the
Sponsor button appears. Sponsorship supports the open maintenance and demo
layer only; it does not unlock private prompts, private canon, customer data,
RPG/TCG material or unreleased proprietary systems.

## Preferred Partner Track

Primary: GitLab.

Reason: GitLab MCP can provide issues, merge requests and pipeline state, which
fits the agent's actual work: safe release readiness and handoff.

Fallback candidates:

- Arize for agent tracing/evaluation.
- Dynatrace for runtime observability.
- MongoDB for evidence store.
- Elastic for searchable logs.

## Demo Narrative

The user asks: "Prepare this public repo for release."

The agent:

1. reads the goal;
2. plans the release-readiness steps;
3. queries partner MCP for project status;
4. writes an observation envelope;
5. returns `APPROVE`, `REVIEW` or `BLOCK`;
6. gives the human the next action instead of silently publishing.
