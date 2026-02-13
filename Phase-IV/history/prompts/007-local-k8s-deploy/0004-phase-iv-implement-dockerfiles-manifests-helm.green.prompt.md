---
id: "0004"
title: "Phase IV Implement: Dockerfiles, Manifests, Helm"
stage: green
date: 2026-02-13
surface: agent
model: claude-sonnet-4-5-20250929
feature: "007-local-k8s-deploy"
branch: "007-local-k8s-deploy"
user: Naz
command: /sp.implement
labels: ["kubernetes","docker","helm","fastapi","nextjs","minikube","devops"]
links:
  spec: specs/007-local-k8s-deploy/spec.md
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - full-stack-todo/frontend/Dockerfile
  - full-stack-todo/frontend/.dockerignore
  - full-stack-todo/backend/Dockerfile
  - full-stack-todo/backend/.dockerignore
  - full-stack-todo/backend/src/main.py
  - full-stack-todo/frontend/next.config.ts
  - docs/phase-iv/kubernetes-manifests/namespace.yaml
  - docs/phase-iv/kubernetes-manifests/backend-deployment.yaml
  - docs/phase-iv/kubernetes-manifests/backend-service.yaml
  - docs/phase-iv/kubernetes-manifests/frontend-deployment.yaml
  - docs/phase-iv/kubernetes-manifests/frontend-service.yaml
  - helm/todo-chatbot/Chart.yaml
  - helm/todo-chatbot/values.yaml
  - helm/todo-chatbot/values-local.yaml
  - helm/todo-chatbot/.helmignore
  - helm/todo-chatbot/templates/_helpers.tpl
  - helm/todo-chatbot/templates/namespace.yaml
  - helm/todo-chatbot/templates/backend-deployment.yaml
  - helm/todo-chatbot/templates/backend-service.yaml
  - helm/todo-chatbot/templates/frontend-deployment.yaml
  - helm/todo-chatbot/templates/frontend-service.yaml
  - docs/phase-iv/README.md
  - docs/phase-iv/containerisation/gordon-session.md
  - docs/phase-iv/kubernetes-manifests/kubectl-ai-session.md
  - docs/phase-iv/helm-chart/helm-session.md
  - docs/phase-iv/aiops/kagent-session.md
  - specs/007-local-k8s-deploy/tasks.md
tests:
  - "null"
---

## Prompt

/sp.implement

(Executed against specs/007-local-k8s-deploy/tasks.md — Phase IV Local Kubernetes Deployment)

## Response snapshot

Executed /sp.implement for Phase IV (007-local-k8s-deploy). Completed the following phases:

**Phase 1 (T001–T002 — Setup)**: Created docs/phase-iv/ directory tree with
containerisation/, kubernetes-manifests/, helm-chart/, aiops/ subdirectories and
session log skeleton files (gordon-session.md, kubectl-ai-session.md, helm-session.md,
kagent-session.md).

**Phase 3 partial (T011–T015 — Containerisation)**:
- Discovered source code is in full-stack-todo/ (not frontend/ / backend/ at root)
- Added `output: "standalone"` to next.config.ts (required for multi-stage Docker build)
- Patched backend/src/main.py: CORS_ORIGINS now read from env var (comma-separated) to
  support dynamic K8s origins
- Generated full-stack-todo/frontend/Dockerfile (node:18-alpine, 3-stage, nextjs user, port 3000)
- Generated full-stack-todo/frontend/.dockerignore
- Generated full-stack-todo/backend/Dockerfile (python:3.11-slim, libpq5 runtime dep, appuser)
- Generated full-stack-todo/backend/.dockerignore
- All Gordon prompts used as primary; Claude Code fallback applied (Gordon region-restricted)

**Phase 4 partial (T021–T027 — K8s Manifests)**:
- Generated namespace.yaml (todo-app namespace)
- Generated backend-deployment.yaml (1 replica, imagePullPolicy: Never, probes on /)
- Generated backend-service.yaml (ClusterIP, port 8000)
- Generated frontend-deployment.yaml (2 replicas, imagePullPolicy: Never, probes on /)
- Generated frontend-service.yaml (NodePort, port 80 → 3000)
- All kubectl-ai prompts used as primary; Claude Code fallback applied

**Phase 5 partial (T030–T031 — Helm Chart)**:
- Generated helm/todo-chatbot/ chart v0.1.0 with Chart.yaml, values.yaml, values-local.yaml
- Generated all 6 Helm templates (namespace, backend-deployment, backend-service,
  frontend-deployment, frontend-service, _helpers.tpl)
- values-local.yaml overrides: pullPolicy: Never, NodePort frontend, reduced Minikube resources
- kubectl-ai prompts used as primary; Claude Code fallback applied

**T045 (Documentation)**: Generated docs/phase-iv/README.md with artefact structure,
AI tool summary, reproduction steps, key config decisions, and known issues.

**Tasks requiring Minikube** (pending user execution):
T003–T009 (env verify), T016–T020 (image build + load), T022 (ConfigMap with DATABASE_URL),
T025, T028–T029 (pod readiness), T032–T036 (helm lint/install/upgrade/rollback),
T037–T041 (kagent AIOps), T042–T044 (final verification + AI ratio).

## Outcome

- ✅ Impact: All static artefacts generated — Dockerfiles, K8s manifests, Helm chart, README. Project is ready for Minikube environment setup and deployment.
- 🧪 Tests: No automated tests (DevOps workflow — CLI verification via kubectl get, helm list, curl). Test criteria documented in each task and README reproduction steps.
- 📁 Files: 27 files created/modified across full-stack-todo/, docs/phase-iv/, helm/, specs/
- 🔁 Next prompts: Run T003–T009 environment verification; then T016–T020 image build/load; then T022 ConfigMap creation with DATABASE_URL; then T034 helm install
- 🧠 Reflection: Source code in full-stack-todo/ (not repo root) required path discovery. CORS must be dynamic env var for K8s. python:3.11-slim required (not alpine) due to psycopg2-binary C-extension. Next.js standalone mode is mandatory for multi-stage Docker. Backend probes use / not /health.

## Evaluation notes (flywheel)

- Failure modes observed: Gordon region-restricted (all docker ai prompts fell back to Claude Code); kubectl-ai requires live Minikube context (fell back to Claude Code for manifest/chart generation); source code location mismatch (full-stack-todo/ vs root)
- Graders run and results (PASS/FAIL): helm lint pending (requires Helm CLI); K8s deployment pending (requires Minikube)
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Run `helm lint ./helm/todo-chatbot` and fix any template issues before deployment
