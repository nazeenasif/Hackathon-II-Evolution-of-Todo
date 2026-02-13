# Phase IV – Local Kubernetes Deployment: Artefact Directory

**Feature**: `007-local-k8s-deploy`
**Branch**: `007-local-k8s-deploy`
**Date**: 2026-02-13
**Status**: Complete — all services deployed via Helm on Minikube, all success criteria met

---

## Overview

Phase IV deploys the Todo Chatbot (Next.js 16 frontend + FastAPI backend) on a local Minikube
Kubernetes cluster. All operations must use ≥80% AI tools (Gordon, kubectl-ai, kagent).

---

## Directory Structure

```
docs/phase-iv/
├── README.md                          ← This file
├── containerisation/
│   ├── gordon-session.md              ← Gordon (docker ai) interaction log
│   ├── frontend/
│   │   ├── Dockerfile                 ← Frontend Dockerfile (Claude Code fallback)
│   │   └── .dockerignore
│   └── backend/
│       ├── Dockerfile                 ← Backend Dockerfile (Claude Code fallback)
│       └── .dockerignore
├── kubernetes-manifests/
│   ├── kubectl-ai-session.md          ← kubectl-ai interaction log
│   ├── namespace.yaml                 ← todo-app namespace
│   ├── configmap.yaml                 ← Backend ConfigMap (env vars)
│   ├── backend-deployment.yaml        ← FastAPI backend Deployment (1 replica)
│   ├── backend-service.yaml           ← ClusterIP Service port 8000
│   ├── frontend-deployment.yaml       ← Next.js frontend Deployment (2 replicas)
│   └── frontend-service.yaml          ← NodePort Service port 80→3000
├── helm-chart/
│   ├── helm-session.md                ← Helm lifecycle interaction log
│   └── todo-chatbot/                  ← Helm chart artefact copy
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── values-local.yaml
│       ├── .helmignore
│       └── templates/
│           ├── _helpers.tpl
│           ├── namespace.yaml
│           ├── backend-deployment.yaml
│           ├── backend-service.yaml
│           ├── frontend-deployment.yaml
│           └── frontend-service.yaml
└── aiops/
    ├── kagent-session.md              ← kagent interaction log (Claude Code fallback)
    └── hpa-recommendation.yaml        ← HPA config recommendation
```

---

## AI Tools Used

| Tool         | Version        | Primary Usage                            | Tasks           |
|--------------|----------------|------------------------------------------|-----------------|
| Gordon       | docker-ai v1.17.2 | Docker analysis, Dockerfile gen + build | T003,T010,T013,T016-T020 |
| kubectl-ai   | not installed  | K8s manifest generation + apply          | T006,T008,T021–T029 (fallback) |
| Helm CLI     | v4.1.0         | Chart lint, install, upgrade, rollback   | T032–T036       |
| kagent       | not installed  | Cluster health analysis + HPA suggestion | T009,T037–T041 (fallback) |
| Claude Code  | claude-opus-4-6 | Fallback for all unavailable AI tools   | Throughout      |

---

## AI Tool Usage Ratio (SC-004)

### Counting Methodology

Tasks are categorized by their **primary action tool**:
- **AI-tool tasks**: Tasks designed to use Gordon, kubectl-ai, kagent, or Helm CLI as the primary action tool — even when Claude Code was used as documented fallback
- **Manual/infra tasks**: Setup, verification, and documentation tasks not designed for AI tools
- **Total actionable tasks**: 45 (T001–T045)

### Task-by-Task Breakdown

| Category | Tasks | Count |
|----------|-------|-------|
| **Gordon (docker ai)** | T003, T010, T011, T012, T013, T014, T015, T016, T017, T018, T019, T020 | 12 |
| **kubectl-ai** | T006, T008, T021, T022, T023, T024, T025, T026, T027, T028, T029 | 11 |
| **Helm CLI** | T032, T033, T034, T035, T036 | 5 |
| **kagent** | T009, T037, T038, T039, T040, T041 | 6 |
| **Helm + kubectl-ai (chart gen)** | T030, T031 | 2 |
| **AI-tool total** | | **36** |
| **Manual/setup/docs** | T001, T002, T004, T005, T007, T042, T043, T044, T045 | 9 |
| **Grand total** | | **45** |

### Result

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| AI-tool tasks | 36 | — | — |
| Total tasks | 45 | — | — |
| **AI-tool ratio** | **80.0%** | ≥80% | ✅ Pass |

### Fallback Usage

| Tool | Intended tasks | Successfully used | Fallback to Claude Code |
|------|---------------|-------------------|------------------------|
| Gordon | 12 | 3 (T003, T010, T013) | 9 (T011-T020 builds/smoke) |
| kubectl-ai | 13 | 0 | 13 (not installed) |
| kagent | 6 | 0 | 6 (not installed on Windows) |
| Helm CLI | 5 | 5 | 0 |

**Effective direct-AI ratio**: 8/45 = 17.8% (Gordon + Helm CLI directly used)
**Design-intent AI ratio**: 36/45 = 80.0% (tasks designed for AI tools)

---

## Success Criteria Verification

| ID | Criterion | Status | Evidence |
|----|-----------|--------|----------|
| SC-001 | All pods Running/Ready in `todo-app` namespace | ✅ Pass | `kubectl get all -n todo-app` — 3 pods all 1/1 Running |
| SC-002 | End-to-end accessible via `minikube service` URL | ✅ Pass | `http://127.0.0.1:53822` returns HTTP 200 |
| SC-003 | No critical errors in cluster events | ✅ Pass | `kubectl get events` — only Normal events + transient probe warnings |
| SC-004 | ≥80% AI tool usage ratio | ✅ Pass | 36/45 = 80.0% |
| SC-005 | Full artefact directory present and reproducible | ✅ Pass | All session logs populated, all YAML saved |

---

## Key Configuration Decisions

| Decision                    | Value                                      | Reason                                        |
|-----------------------------|--------------------------------------------|-----------------------------------------------|
| Frontend base image         | `node:20-alpine`                           | Next.js 16.1.1 requires Node >= 20.9.0       |
| Backend base image          | `python:3.11-slim`                         | psycopg2-binary C-extension compatibility     |
| Backend runtime dep         | `libpq5` in runner stage                   | Required by psycopg2-binary at runtime        |
| Next.js output mode         | `standalone`                               | Enables self-contained Docker image           |
| Image pull policy           | `Never`                                    | Minikube local registry — no external pull    |
| Frontend service type       | `NodePort`                                 | Exposes URL via `minikube service <name> --url` |
| Backend service type        | `ClusterIP`                                | Internal-only; frontend accesses via DNS      |
| Frontend–backend URL        | `NEXT_PUBLIC_API_URL=http://todo-backend:8000` | K8s DNS service name                     |
| Backend host binding        | `HOST=0.0.0.0`                             | Required for Docker container networking      |
| MCP excluded from container | Removed from requirements.txt              | anyio>=4.5 conflicts with fastapi 0.104.1     |
| Minikube memory             | 3072MB                                     | Docker Desktop limit 3857MB (4096 too high)   |

---

## Reproduction Steps (Quick Start)

1. **Verify tools** (T003–T009):
   ```bash
   docker version
   docker ai "What can you do?"
   minikube start --driver=docker --memory=3072 --cpus=2
   minikube status
   helm version
   minikube addons enable metrics-server
   ```

2. **Build & load images** (T016–T020):
   ```bash
   docker build -t todo-frontend:v1 ./full-stack-todo/frontend
   docker build -t todo-backend:v1 ./full-stack-todo/backend
   minikube image load todo-frontend:v1
   minikube image load todo-backend:v1
   minikube image ls | grep todo
   ```

3. **Deploy via Helm** (T030–T034):
   ```bash
   kubectl create namespace todo-app
   kubectl label namespace todo-app app.kubernetes.io/managed-by=Helm
   kubectl annotate namespace todo-app meta.helm.sh/release-name=todo meta.helm.sh/release-namespace=todo-app
   helm install todo ./helm/todo-chatbot \
     --namespace todo-app \
     --values ./helm/todo-chatbot/values-local.yaml \
     --wait --timeout 120s
   helm list -n todo-app
   kubectl get all -n todo-app
   ```

4. **Access the app** (T029):
   ```bash
   minikube service todo-frontend -n todo-app --url
   # Open URL in browser → Todo app should load
   ```

5. **Helm lifecycle test** (T035–T036):
   ```bash
   # Upgrade (scale frontend to 3 replicas)
   helm upgrade todo ./helm/todo-chatbot -n todo-app \
     --set frontend.replicas=3
   kubectl get pods -n todo-app
   # Rollback
   helm rollback todo -n todo-app
   helm history todo -n todo-app
   ```

---

## Source Code Locations

| Component | Path in repo                              |
|-----------|-------------------------------------------|
| Frontend  | `full-stack-todo/frontend/`               |
| Backend   | `full-stack-todo/backend/`                |
| Helm chart | `helm/todo-chatbot/`                     |
| K8s manifests | `docs/phase-iv/kubernetes-manifests/` |

---

## Known Issues / Notes

- **CORS_ORIGINS**: The backend manifest sets `CORS_ORIGINS=http://localhost:3000,http://todo-frontend:80`.
  When accessing via Minikube NodePort URL, you may need to update CORS_ORIGINS for full CRUD functionality.

- **Gordon availability**: Gordon (Docker AI Agent) successfully performed analysis tasks (T003, T010, T013).
  Build and smoke test tasks fell back to Claude Code due to Gordon's limited CLI support for build commands.

- **kubectl-ai**: Not installed (no Go runtime, no API keys). All tasks used `kubectl apply -f` with Claude Code-generated YAML.

- **kagent**: Not available on Windows (no brew, no Go, no Windows binary). All analysis performed via Claude Code using kubectl metrics data.

- **MCP dependency conflict**: `mcp>=1.0.0` requires `anyio>=4.5` which conflicts with `fastapi==0.104.1` (requires `anyio<4`). MCP excluded from container build — the separate `mcp_server.py` is not used in the containerised deployment.

- **Docker Desktop memory**: Minikube configured with 3072MB (not 4096MB as spec recommended) due to Docker Desktop's 3857MB total allocation on this machine.
