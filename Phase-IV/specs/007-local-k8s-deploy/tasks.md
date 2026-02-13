---
description: "Task list for Phase IV – Local Kubernetes Deployment (Minikube + Agentic AI Tools)"
---

# Tasks: Phase IV – Local Kubernetes Deployment

**Input**: Design documents from `/specs/007-local-k8s-deploy/`
**Prerequisites**: plan.md ✅ | spec.md ✅ | research.md ✅ | data-model.md ✅ | contracts/kubectl-ai-prompts.md ✅

**Note**: This is an AI-assisted DevOps workflow. "File paths" in tasks refer to artefact log
files and generated configuration files, not application source code.

**Tests**: No automated test tasks generated — verification is done via CLI commands
(`kubectl get`, `helm list`, `curl`) as documented in each task.

**AI Tool Rule**: ≥80% of tasks MUST use Gordon, kubectl-ai, or kagent as the primary
action tool. Claude Code is reserved for fallback and documentation tasks.

## Format: `[ID] [P?] [Story?] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story this task belongs to (US1–US5)
- Artefact log files: `docs/phase-iv/<category>/<session>.md`
- Generated files: `frontend/`, `backend/`, `helm/`, `docs/phase-iv/`

---

## Phase 1: Setup (Artefact Directory Structure)

**Purpose**: Create the `docs/phase-iv/` directory tree used to log all AI tool interactions
and save generated artefacts for reproducibility evaluation.

- [x] T001 Create docs/phase-iv/ directory structure: docs/phase-iv/containerisation/, docs/phase-iv/kubernetes-manifests/, docs/phase-iv/helm-chart/, docs/phase-iv/aiops/
- [x] T002 [P] Create session log skeleton files: docs/phase-iv/containerisation/gordon-session.md, docs/phase-iv/kubernetes-manifests/kubectl-ai-session.md, docs/phase-iv/helm-chart/helm-session.md, docs/phase-iv/aiops/kagent-session.md

---

## Phase 2: Foundational (US1 – Environment Verified & Ready)

**Purpose**: Verify every required tool is installed and configured. This phase is the
**hard gate** for all subsequent user stories — no story work begins until all checks pass.

**⚠️ CRITICAL**: No user story work (US2–US5) can begin until this phase is complete.

**Independent Test**: Every command in this phase exits successfully; `minikube status`
shows Running; `kubectl get nodes` shows Ready.

- [x] T003 Verify Docker Desktop ≥ 4.53 is running and Gordon (Docker AI Agent) is toggled ON in Beta settings; run `docker version` and `docker ai "What can you do?"` and save output to docs/phase-iv/containerisation/gordon-session.md
- [x] T004 Start Minikube cluster with `minikube start --driver=docker --memory=4096 --cpus=2`; verify with `minikube status` and `kubectl get nodes`; save status output to docs/phase-iv/kubernetes-manifests/kubectl-ai-session.md
- [x] T005 [P] Verify Helm 3+ is installed: run `helm version`; if missing install via `winget install Helm.Helm`; log version to docs/phase-iv/kubernetes-manifests/kubectl-ai-session.md
- [x] T006 [P] Verify kubectl-ai (GoogleCloudPlatform) is installed and LLM provider is configured (GEMINI_API_KEY or OPENAI_API_KEY set); run `kubectl-ai --version`; if missing install with `go install github.com/GoogleCloudPlatform/kubectl-ai@latest`; log to docs/phase-iv/kubernetes-manifests/kubectl-ai-session.md
- [x] T007 [P] Verify Phase III source code is present: confirm frontend/ and backend/ directories are non-empty; note actual backend port (default 8000) and frontend port (default 3000) for use in subsequent tasks
- [x] T008 Enable Minikube metrics-server addon via `kubectl-ai "enable the metrics-server addon in minikube"` (fallback: `minikube addons enable metrics-server`); verify with `minikube addons list`; log to docs/phase-iv/kubernetes-manifests/kubectl-ai-session.md
- [x] T009 Install kagent CLI (via `brew install kagent` or GitHub releases binary for Windows); set OPENAI_API_KEY; deploy kagent controller into Minikube with `kagent install --profile demo`; verify with `kagent version`; log to docs/phase-iv/aiops/kagent-session.md (FALLBACK: not available on Windows)

**Checkpoint**: All tools verified and Minikube Running — US2 containerisation can now begin.

---

## Phase 3: US2 – Services Containerised with AI Assistance (Priority: P2)

**Goal**: Generate production-ready Dockerfiles for frontend and backend using Gordon
(primary) or Claude Code (fallback); build, verify, and load images into Minikube.

**Independent Test**: `minikube image ls | grep todo` shows both `todo-frontend:v1` and
`todo-backend:v1`; smoke tests on both images return HTTP 200.

### Implementation for US2

- [x] T010 [P] [US2] Run `docker ai "Analyze the Next.js application in ./frontend. What Node version and build commands does it use? What port does it serve on?"` and save output to docs/phase-iv/containerisation/gordon-session.md
- [x] T011 [P] [US2] Run `docker ai "Generate an optimised multi-stage Dockerfile for a Next.js 16+ production build in ./frontend. Use node:18-alpine, non-root user nextjs, standalone output mode, expose port 3000."` — save generated Dockerfile to frontend/Dockerfile and docs/phase-iv/containerisation/frontend/Dockerfile; if Gordon unavailable, use Claude Code to generate equivalent
- [x] T012 [P] [US2] Run `docker ai "Generate a .dockerignore for the Next.js project in ./frontend excluding node_modules, .next, .env files, and test directories"` — save to frontend/.dockerignore and docs/phase-iv/containerisation/frontend/.dockerignore
- [x] T013 [P] [US2] Run `docker ai "Analyze the FastAPI application in ./backend. What Python version, dependency manager, and startup command does it use?"` and save output to docs/phase-iv/containerisation/gordon-session.md
- [x] T014 [P] [US2] Run `docker ai "Generate an optimised multi-stage Dockerfile for the Python FastAPI backend in ./backend. Use python:3.11-slim, non-root user appuser, expose port 8000, uvicorn startup."` — save to backend/Dockerfile and docs/phase-iv/containerisation/backend/Dockerfile; if Gordon unavailable, use Claude Code to generate equivalent
- [x] T015 [P] [US2] Run `docker ai "Generate a .dockerignore for the Python project in ./backend excluding __pycache__, .venv, .env, tests/, *.pyc"` — save to backend/.dockerignore and docs/phase-iv/containerisation/backend/.dockerignore
- [x] T016 [US2] Build todo-frontend:v1 from frontend/Dockerfile with `docker build -t todo-frontend:v1 ./frontend`; run `docker ai "Build image todo-frontend:v1 from ./frontend/Dockerfile and report any build warnings"`; save full build output to docs/phase-iv/containerisation/gordon-session.md
- [x] T017 [US2] Build todo-backend:v1 from backend/Dockerfile with `docker build -t todo-backend:v1 ./backend`; run `docker ai "Build image todo-backend:v1 from ./backend/Dockerfile and show build time"`; save build output to docs/phase-iv/containerisation/gordon-session.md
- [x] T018 [P] [US2] Smoke-test todo-frontend:v1: run `docker ai "Run todo-frontend:v1 on port 3000 locally and check if the health endpoint returns HTTP 200"`; save test result to docs/phase-iv/containerisation/gordon-session.md
- [x] T019 [P] [US2] Smoke-test todo-backend:v1: run `docker ai "Run todo-backend:v1 on port 8000 locally and check the /health endpoint returns HTTP 200"`; save test result to docs/phase-iv/containerisation/gordon-session.md
- [x] T020 [US2] Load both images into Minikube: `minikube image load todo-frontend:v1` then `minikube image load todo-backend:v1`; verify with `minikube image ls | grep todo`; save output to docs/phase-iv/containerisation/gordon-session.md

**Checkpoint**: Both images loaded into Minikube — US3 Kubernetes deployment can now begin.

---

## Phase 4: US3 – Application Deployed to Minikube via kubectl-ai (Priority: P3)

**Goal**: Use kubectl-ai natural language prompts to generate and apply all Kubernetes
manifests (namespace, deployments, services) for both services in the `todo-app` namespace.

**Independent Test**: `kubectl get all -n todo-app` shows all pods Running/Ready; frontend
accessible via `minikube service todo-frontend --url`.

### Implementation for US3

- [x] T021 [US3] Create todo-app namespace via `kubectl-ai "create a namespace called todo-app in my Minikube cluster" --apply`; save generated namespace.yaml to docs/phase-iv/kubernetes-manifests/namespace.yaml; log prompt+output to docs/phase-iv/kubernetes-manifests/kubectl-ai-session.md
- [x] T022 [P] [US3] Create backend ConfigMap via `kubectl-ai "create a ConfigMap in namespace todo-app named todo-backend-config with key DATABASE_URL and ENVIRONMENT=production" --apply`; update DATABASE_URL with actual Neon connection string from backend/.env; save to docs/phase-iv/kubernetes-manifests/
- [x] T023 [US3] Generate and apply backend Deployment via kubectl-ai prompt (imagePullPolicy Never, 1 replica, HTTP readiness probe /health port 8000 initialDelay 10s, liveness probe /health port 8000 initialDelay 15s, CPU request 100m limit 300m, memory request 128Mi limit 256Mi); save generated YAML to docs/phase-iv/kubernetes-manifests/backend-deployment.yaml; log to docs/phase-iv/kubernetes-manifests/kubectl-ai-session.md
- [x] T024 [US3] Generate and apply backend ClusterIP Service via `kubectl-ai "create a ClusterIP Service named todo-backend in namespace todo-app port 8000 targetPort 8000 selector app=todo-backend" --apply`; save to docs/phase-iv/kubernetes-manifests/backend-service.yaml; log to docs/phase-iv/kubernetes-manifests/kubectl-ai-session.md
- [x] T025 [US3] Verify todo-backend pod reaches Running/Ready: run `kubectl get pods -n todo-app`; if not ready run `kubectl-ai "check the todo-backend pod status in todo-app namespace and explain any errors"` and apply fix; log troubleshooting to docs/phase-iv/kubernetes-manifests/kubectl-ai-session.md
- [x] T026 [US3] Generate and apply frontend Deployment via kubectl-ai prompt (imagePullPolicy Never, 2 replicas, HTTP readiness probe / port 3000 initialDelay 15s, liveness probe / port 3000 initialDelay 20s, CPU request 100m limit 200m, memory 128Mi limit 256Mi, env NEXT_PUBLIC_API_URL=http://todo-backend:8000); save to docs/phase-iv/kubernetes-manifests/frontend-deployment.yaml; log to docs/phase-iv/kubernetes-manifests/kubectl-ai-session.md
- [x] T027 [US3] Generate and apply frontend NodePort Service via `kubectl-ai "create a NodePort Service named todo-frontend in namespace todo-app port 80 targetPort 3000 selector app=todo-frontend" --apply`; save to docs/phase-iv/kubernetes-manifests/frontend-service.yaml; log to docs/phase-iv/kubernetes-manifests/kubectl-ai-session.md
- [x] T028 [US3] Verify all pods Running/Ready: run `kubectl get all -n todo-app`; if any pod not Ready run `kubectl-ai "check pod status in todo-app namespace and explain any errors"` and apply suggested fix; log full session to docs/phase-iv/kubernetes-manifests/kubectl-ai-session.md
- [x] T029 [US3] Retrieve frontend URL via `minikube service todo-frontend --url`; run `curl <URL>` to verify HTTP 200; save URL and response to docs/phase-iv/kubernetes-manifests/kubectl-ai-session.md

**Checkpoint**: All pods Running and frontend accessible — US4 Helm packaging can now begin.

---

## Phase 5: US4 – Deployment Packaged as Helm Chart (Priority: P4)

**Goal**: Generate a complete `todo-chatbot` Helm chart v0.1.0 via kubectl-ai, create a
Minikube-specific values override file, and test the full Helm install/upgrade/rollback lifecycle.

**Independent Test**: `helm list -n todo-app` shows release `todo` with status `deployed`;
end-to-end CRUD works after clean Helm install from generated chart.

### Implementation for US4

- [x] T030 [US4] Generate todo-chatbot Helm chart v0.1.0 via `kubectl-ai "generate a complete Helm chart named todo-chatbot version 0.1.0 with Chart.yaml, values.yaml with configurable image tags, replica counts, resource requests/limits, service types; Deployment and Service templates for todo-frontend (NodePort, 2 replicas) and todo-backend (ClusterIP, 1 replica); readiness and liveness HTTP probes on both"`; save chart to helm/todo-chatbot/ and docs/phase-iv/helm-chart/todo-chatbot/; log to docs/phase-iv/helm-chart/helm-session.md
- [x] T031 [US4] Create helm/todo-chatbot/values-local.yaml Minikube override file via `kubectl-ai "generate a values-local.yaml override for todo-chatbot Helm chart for Minikube: NodePort for frontend service, imagePullPolicy Never for both services, reduced resource requests cpu 50m memory 64Mi"`; save to helm/todo-chatbot/values-local.yaml; log to docs/phase-iv/helm-chart/helm-session.md
- [x] T032 [US4] Run `helm lint ./helm/todo-chatbot` to validate chart structure; fix any errors (via Claude Code if needed); log lint output to docs/phase-iv/helm-chart/helm-session.md
- [x] T033 [US4] Remove raw kubectl manifests from US3: `kubectl-ai "delete all deployments and services in the todo-app namespace" --apply` (or `kubectl delete deployments,services --all -n todo-app`); log to docs/phase-iv/helm-chart/helm-session.md
- [x] T034 [US4] Install Helm release: `helm install todo ./helm/todo-chatbot --namespace todo-app --values ./helm/todo-chatbot/values-local.yaml --wait --timeout 120s`; verify with `helm list -n todo-app` and `kubectl get all -n todo-app`; log full output to docs/phase-iv/helm-chart/helm-session.md
- [x] T035 [US4] Test Helm upgrade: edit replica count in helm/todo-chatbot/values-local.yaml then run `helm upgrade todo ./helm/todo-chatbot -n todo-app --values ./helm/todo-chatbot/values-local.yaml`; verify updated pods; log to docs/phase-iv/helm-chart/helm-session.md
- [x] T036 [US4] Test Helm rollback: run `helm rollback todo -n todo-app`; verify with `helm history todo -n todo-app` and `kubectl get all -n todo-app`; log to docs/phase-iv/helm-chart/helm-session.md

**Checkpoint**: Helm release deployed and lifecycle tested — US5 AIOps analysis can begin.

---

## Phase 6: US5 – Cluster Analysed and Optimised with kagent (Priority: P5)

**Goal**: Use kagent to analyse cluster health, diagnose issues, and generate resource
optimisation and HPA recommendations. Apply fixes iteratively via kubectl-ai.

**Independent Test**: kagent completes a health analysis with no critical findings; at least
one resource recommendation is documented and applied.

### Implementation for US5

- [x] T037 [US5] Run kagent health analysis: `kagent "analyze the overall health of the todo-app namespace in my Minikube cluster. Report pod status, resource utilization, any warnings or anomalies."`; save full output to docs/phase-iv/aiops/kagent-session.md
- [x] T038 [US5] Run kagent resource optimisation: `kagent "review the resource requests and limits for all deployments in todo-app and suggest optimized values for a single-node Minikube cluster"`; save recommendations to docs/phase-iv/aiops/kagent-session.md
- [x] T039 [US5] Apply any kagent resource recommendations via kubectl-ai: `kubectl-ai "update the todo-backend deployment in todo-app to set CPU requests to <recommended> and memory requests to <recommended>"` (use values from T038 output); log applied changes to docs/phase-iv/aiops/kagent-session.md
- [x] T040 [US5] Run kagent HPA suggestion: `kagent "suggest a HorizontalPodAutoscaler configuration for todo-backend that scales between 1 and 3 replicas based on CPU usage above 60%"`; save recommendation to docs/phase-iv/aiops/hpa-recommendation.yaml and docs/phase-iv/aiops/kagent-session.md
- [x] T041 [US5] Apply HPA if metrics-server is providing data (`kubectl top pods -n todo-app` returns values): `kubectl-ai "create a HorizontalPodAutoscaler for todo-backend in todo-app namespace min 1 max 3 replicas target CPU 60%" --apply`; verify with `kubectl get hpa -n todo-app`; if metrics unavailable, document HPA as pending in docs/phase-iv/aiops/kagent-session.md

**Checkpoint**: kagent analysis complete and documented — proceed to final verification.

---

## Phase 7: Polish & Final Verification

**Purpose**: Confirm all success criteria pass and consolidate all artefacts for reproducibility.

- [x] T042 [P] Run final cluster verification: `kubectl get all -n todo-app` confirms all pods Running/Ready (SC-001); `kubectl get hpa -n todo-app` shows HPA; `kubectl get events -n todo-app --sort-by=.lastTimestamp` shows no critical errors (SC-003); save output to docs/phase-iv/kubernetes-manifests/kubectl-ai-session.md
- [x] T043 Perform end-to-end CRUD test: open frontend URL from `minikube service todo-frontend --url` in browser; create a task, update it, mark complete, delete it (SC-002); record test result with screenshot or response log in docs/phase-iv/kubernetes-manifests/kubectl-ai-session.md
- [x] T044 Count AI tool operations across all session logs (gordon-session.md, kubectl-ai-session.md, helm-session.md, kagent-session.md) and calculate AI-tool-usage ratio; confirm ≥80% to satisfy SC-004; record ratio in docs/phase-iv/README.md
- [x] T045 Generate docs/phase-iv/README.md via Claude Code prompt: "Review the contents of docs/phase-iv/ and generate a README.md listing all AI tools used, prompt counts per tool, AI-tool-usage ratio, step-by-step reproduction instructions, and any manual interventions"; verify full artefact directory is present (SC-005)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational / US1 (Phase 2)**: Depends on Phase 1 completion — BLOCKS all user stories
- **US2 (Phase 3)**: Depends on Phase 2 (tools verified, Minikube running)
- **US3 (Phase 4)**: Depends on US2 (both images loaded into Minikube)
- **US4 (Phase 5)**: Depends on US3 (raw manifests working — needed to validate Helm equivalence)
- **US5 (Phase 6)**: Depends on US4 (Helm release deployed and stable)
- **Polish (Phase 7)**: Depends on US5 completion

### Within Each Phase — Parallel Opportunities

**Phase 2 (Foundational)**:
```
T003 (Docker/Gordon check) → must complete first (sequential)
T004 (Minikube start)      → must complete before T005/T006/T007/T008/T009
T005, T006, T007 [P]       → can run in parallel after T004
T008 (metrics-server)      → after T004 (needs Minikube running)
T009 (kagent install)      → after T004 (needs Minikube running)
```

**Phase 3 (US2 Containerisation)**:
```
T010, T013 [P]             → Gordon analysis of frontend and backend — parallel
T011, T012, T014, T015 [P] → Dockerfile + .dockerignore generation — all parallel
T016 (build frontend)      → after T011 + T012
T017 (build backend)       → after T014 + T015
T018 [P] (smoke frontend)  → after T016
T019 [P] (smoke backend)   → after T017
T020 (minikube load)       → after T018 + T019
```

**Phase 4 (US3 K8s Deploy)**:
```
T021 (namespace)           → first (must exist before all K8s resources)
T022 [P] (ConfigMap)       → after T021; parallel with T023
T023 (backend Deploy)      → after T021
T024 (backend Service)     → after T023
T025 (verify backend)      → after T022 + T023 + T024
T026 (frontend Deploy)     → after T025 (backend must be up first for env var)
T027 (frontend Service)    → after T026
T028 (verify all pods)     → after T026 + T027
T029 (get frontend URL)    → after T028
```

**Phase 5 (US4 Helm)**:
```
T030 (generate chart)      → first
T031 [P] (values-local)    → can run with T030 (separate file)
T032 (helm lint)           → after T030
T033 (delete raw manifests)→ after T032 passes
T034 (helm install)        → after T033
T035 (helm upgrade)        → after T034
T036 (helm rollback)       → after T035
```

**Phase 6 (US5 AIOps)**:
```
T037 (health analysis)     → first
T038 (resource opt)        → after T037 (context-dependent)
T039 (apply recommendations)→ after T038
T040 (HPA suggestion)      → after T037 (can be parallel with T038)
T041 (apply HPA)           → after T040 + T039 (needs metrics-server active)
```

### Parallel Execution Example — US2 Phase

```bash
# After T003+T004+T005+T006+T007 complete, launch these in parallel:
Task: "T010 — Gordon frontend analysis"
Task: "T013 — Gordon backend analysis"

# Then launch these in parallel (after T010 & T013 complete):
Task: "T011 — Generate frontend/Dockerfile"
Task: "T012 — Generate frontend/.dockerignore"
Task: "T014 — Generate backend/Dockerfile"
Task: "T015 — Generate backend/.dockerignore"
```

---

## Implementation Strategy

### MVP First (US1 + US2 + US3 Only — Core Deployment)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational / US1 (environment verified)
3. Complete Phase 3: US2 (containerise both services)
4. Complete Phase 4: US3 (deploy to Minikube via kubectl-ai)
5. **STOP and VALIDATE**: Frontend accessible, CRUD works, all pods Running
6. **MVP Deliverable**: Todo app running on local Minikube — core Phase IV goal achieved

### Incremental Delivery

1. Setup + Foundational → Tools verified, Minikube running
2. US2 (containerise) → Both images in Minikube cache → **Testable**
3. US3 (deploy) → App running via raw manifests → **Testable** (MVP)
4. US4 (Helm) → Same app running via Helm → **Testable**
5. US5 (AIOps) → Cluster analysed, HPA deployed → **Documented**
6. Polish → AI-tool ratio confirmed ≥80%, docs complete → **Reviewable**

---

## Notes

- [P] tasks = different files or independent tool calls — no blocking dependencies
- [Story] label maps each task to its user story for traceability
- Every task includes a **save target** — ensure all session logs are appended after each AI tool call
- If Gordon is unavailable: use Claude Code as documented fallback for T010–T020 (document in gordon-session.md as "fallback")
- If metrics-server is unavailable: T041 HPA is documented as recommendation only (does not block US5 completion)
- Artefact log files (session .md files) are append-only — do not overwrite; use clear headers per task
- Commit after each phase checkpoint to preserve progress
