---
id: 0001
title: Phase IV Kubernetes Deployment Spec
stage: spec
date: 2026-02-13
surface: agent
model: claude-sonnet-4-5-20250929
feature: 007-local-k8s-deploy
branch: 007-local-k8s-deploy
user:
command: /sp.specify
labels: [spec, kubernetes, minikube, docker, helm, kubectl-ai, kagent, phase-iv, aiops]
links:
  spec: specs/007-local-k8s-deploy/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/007-local-k8s-deploy/spec.md
 - specs/007-local-k8s-deploy/checklists/requirements.md
 - history/prompts/007-local-k8s-deploy/0001-phase-iv-kubernetes-deployment-spec.spec.prompt.md
tests:
 -
---

## Prompt

```
/sp.specify

Project: Cloud Native Todo Chatbot – Phase IV: Local Kubernetes Deployment using Minikube + Agentic AI Tools

Phase Goal (high-level objective):
Deploy the Phase III Todo Chatbot (frontend + backend) on a local Minikube Kubernetes cluster using:
- Docker containerization with Gordon AI assistance (or fallback to standard Docker/Claude Code)
- Helm Charts for packaging and deployment
- kubectl-ai for generating & applying Kubernetes manifests/commands via natural language
- kagent for advanced cluster analysis, troubleshooting, and optimization
- Strictly follow Agentic Dev Stack: No manual coding allowed → all generation and operations via Claude Code / AI agents

Core Spec Principles:
- 100% agent-assisted where possible: Maximize use of natural language prompts with Gordon (docker ai "..."), kubectl-ai, kagent
- Workflow: Write detailed spec → Generate step-by-step plan → Break into small executable tasks → Implement via Claude Code iterations
- Local-only environment: Minikube (single-node cluster via Docker driver), Docker Desktop
- Reproducibility for review: Log/save EVERY AI prompt used, generated artifacts (Dockerfiles, Helm charts, manifests), commands executed, and outputs/errors
- Basic production-grade elements: Health/readiness/liveness probes, resource requests/limits, multiple replicas (frontend: 2–3, backend: 1–3 with scaling potential), services properly exposed

Detailed Requirements & Acceptance Criteria:

1. Environment Setup Verification
   - Docker Desktop ≥ 4.53+ with Beta features enabled → Docker AI Agent (Gordon) toggled on
   - Minikube installed & started: minikube start --driver=docker
   - Helm 3+ installed
   - kubectl-ai installed (preferred: GoogleCloudPlatform version) and configured with LLM provider
   - kagent installed & configured (CLI via brew or curl, with LLM provider set)
   - Phase III Todo Chatbot source code available (separate frontend & backend directories/services)

2. Containerization with Gordon
   - Maximize Gordon usage for Dockerfile generation
   - Fallback if Gordon unavailable: Use Claude Code
   - Final local images: todo-frontend:v1 and todo-backend:v1

3. Kubernetes Manifests & Deployment via kubectl-ai
   - Natural language K8s manifests via kubectl-ai
   - 2 replicas frontend, 1–3 backend
   - Health probes, resource requests/limits

4. Helm Chart Generation & Installation (AI-assisted)
   - Chart todo-chatbot v0.1.0 with values-local.yaml for Minikube
   - Install, upgrade, rollback support

5. AIOps & Optimization with kagent
   - Cluster health analysis, pod diagnostics, resource optimisation
   - HPA recommendation

6. Final Verification
   - All pods Running/Ready
   - End-to-end CRUD works
   - ≥80% operations via AI tools
   - Full documentation saved
```

## Response snapshot

```
Created branch 007-local-k8s-deploy and spec at specs/007-local-k8s-deploy/spec.md.

Spec contains:
- 5 prioritised user stories (P1 env setup, P2 containerise, P3 K8s deploy, P4 Helm, P5 kagent AIOps)
- 6 edge cases (Gordon fallback, ImagePullBackOff, CrashLoopBackOff, resource overload,
  invalid YAML, Helm failure recovery)
- 12 functional requirements (FR-001–FR-012)
- 6 key entities (Container Image, K8s Deployment, K8s Service, Helm Chart, AI Interaction Log,
  Namespace)
- 7 success criteria (SC-001–SC-007) with measurable thresholds
- 7 assumptions documented

Quality checklist at specs/007-local-k8s-deploy/checklists/requirements.md: PASS (all items).
No [NEEDS CLARIFICATION] markers — input was sufficiently detailed.
```

## Outcome

- ✅ Impact: Full Phase IV spec created with 5 user stories covering environment setup through
  AIOps optimisation; checklist passes all quality gates
- 🧪 Tests: No tests — spec stage
- 📁 Files: specs/007-local-k8s-deploy/spec.md, specs/007-local-k8s-deploy/checklists/requirements.md
- 🔁 Next prompts: /sp.plan to generate architecture and implementation plan
- 🧠 Reflection: The spec successfully captures the dual nature of Phase IV: it is both an
  infrastructure deployment spec AND an AI tooling demonstration spec. The ≥80% AI-tool-usage
  criterion (FR-011/SC-004) is the key differentiator from a standard deployment spec.

## Evaluation notes (flywheel)

- Failure modes observed: create-new-feature.ps1 errored on "prompts" argument but branch and
  spec file were created successfully before the error; history/prompts dir created manually
- Graders run and results (PASS/FAIL): PASS — no unresolved placeholders, all mandatory sections
  present, 5 user stories cover full deployment lifecycle
- Prompt variant (if applicable): Standard /sp.specify with detailed user input
- Next experiment (smallest change to try): Run /sp.plan to generate architecture plan for
  007-local-k8s-deploy
