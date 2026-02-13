# Research: Phase IV – Local Kubernetes Deployment

**Feature**: `007-local-k8s-deploy`
**Date**: 2026-02-13
**Purpose**: Resolve all technical unknowns from plan Technical Context before Phase 1 design.

---

## R-001 — Frontend Container Base Image

**Decision**: `node:18-alpine` for build stage; `node:18-alpine` for runtime stage
(multi-stage build). Use Next.js `output: 'standalone'` mode in `next.config.js`.

**Rationale**: Alpine images are ~50–70% smaller than full Debian variants. Standalone output
mode copies only the required server files and avoids shipping the full `node_modules` into the
runtime layer.

**Recommended Dockerfile pattern**:
```
Stage 1 (deps):    node:18-alpine — install production deps only
Stage 2 (builder): node:18-alpine — copy deps, copy source, run `next build`
Stage 3 (runner):  node:18-alpine — copy standalone output + public + static,
                   create non-root user `nextjs` (uid 1001), EXPOSE 3000,
                   CMD ["node", "server.js"]
```

**Non-root user setup**:
```dockerfile
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
USER nextjs
```

**Alternatives Considered**:
- `node:18` (full Debian): 350 MB vs ~120 MB for alpine; rejected for size.
- `node:18-slim`: smaller than full but larger than alpine; no benefit over alpine here.

---

## R-002 — Backend Container Base Image

**Decision**: `python:3.11-slim` for both build and runtime stages (or single stage for
simplicity). If the team uses `uv` package manager, `ghcr.io/astral-sh/uv:python3.11-slim`
is an alternative.

**Rationale**: `python:3.11-slim` is the official recommended production image for Python
applications. It is ~130 MB vs ~900 MB for full Debian. Alpine (`python:3.11-alpine`) has
known C-extension compatibility issues with some pip packages (e.g., psycopg2) and requires
additional build tools.

**Recommended Dockerfile pattern**:
```
Stage 1 (builder): python:3.11-slim — install build tools, create venv, pip install
Stage 2 (runtime): python:3.11-slim — copy venv from builder, copy source,
                   create non-root user `appuser` (uid 1001),
                   EXPOSE 8000,
                   CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Non-root user setup**:
```dockerfile
RUN useradd --system --uid 1001 --no-create-home appuser
USER appuser
```

**Alternatives Considered**:
- `python:3.11-alpine`: Smaller but C-extension issues; rejected for reliability.
- `python:3.11`: Full Debian, too large; rejected.

---

## R-003 — Loading Local Images into Minikube (Windows, Docker Driver)

**Decision**: Use `minikube image load <image>:<tag>` for Windows with Docker driver.

**Rationale**: On Windows with the Docker driver, Minikube runs inside Docker. The
`eval $(minikube docker-env)` approach requires a Bash shell and environment variable
inheritance, which is unreliable in PowerShell/Windows terminals. `minikube image load`
directly copies a locally-built Docker image into the Minikube container's image cache,
which works reliably across all operating systems.

**Critical**: After loading, set `imagePullPolicy: Never` in all Deployment specs. If
`imagePullPolicy: Always` is used, Kubernetes will attempt to pull from a registry and fail
since the image is only in the local cache.

**Verification after load**:
```bash
minikube image ls | grep todo
```

**Alternatives Considered**:
- `eval $(minikube docker-env)` + `docker build`: Cross-platform issues on Windows; rejected.
- Pushing to a local registry (e.g., registry:2 in Minikube): Works but adds complexity and
  registry management overhead; rejected for simplicity.

---

## R-004 — kubectl-ai (GoogleCloudPlatform) — Installation & Configuration

**Decision**: Install via Go: `go install github.com/GoogleCloudPlatform/kubectl-ai@latest`

**LLM Configuration** (set before use):
```bash
# Option A — Gemini (recommended, free tier available):
export GEMINI_API_KEY="your-key-here"

# Option B — OpenAI:
export OPENAI_API_KEY="your-key-here"
export OPENAI_MODEL="gpt-4o"   # optional, defaults to gpt-4o
```

**Key flags**:
- `--apply` — applies generated YAML directly to the cluster without a confirmation step
- Without `--apply` — shows generated YAML and asks for confirmation (safer for review)
- `--cluster` — specifies target cluster (defaults to current kubectl context)

**Usage pattern for this project** (recommended: review before apply):
```bash
kubectl-ai "<natural language prompt>"    # Review generated YAML
# → Y to apply, or save to file first
```

**Alternatives Considered**:
- `k8sgpt`: Focused on diagnostics rather than manifest generation; retained kagent for that.
- Manual YAML authoring: Violates Principle II (Agentic Dev Stack); rejected.

---

## R-005 — kagent — Installation & Configuration

**Decision**: kagent is a **Kubernetes-native controller** (not a standalone CLI binary).
Install the CLI via Homebrew (or binary from GitHub releases for Windows), then deploy the
controller into Minikube with `kagent install`.

**Architecture**:
- **CLI** (`kagent`) — local client that manages agents and runs queries
- **Controller** — deployed into the cluster as K8s custom resources
- **Engine** — runs AI agents using LLM providers (OpenAI, Anthropic, Gemini, Ollama)
- **ToolServers** — built-in MCP tools for Kubernetes, Helm, Prometheus, etc.

**Install (macOS/Linux via Homebrew)**:
```bash
brew install kagent
kagent install --profile demo    # deploys controller into Minikube cluster
```

**Install (Windows — no native brew)**:
```bash
# Option A: WSL2 with Homebrew
brew install kagent

# Option B: Download binary from GitHub releases
# https://github.com/kagent-dev/kagent/releases
# Place kagent.exe in PATH

# Option C: pip install (if Python distribution available)
pip install kagent
```

**LLM Configuration** (required before `kagent install`):
```bash
export OPENAI_API_KEY="your-key-here"
# kagent supports: OpenAI, Azure OpenAI, Anthropic, Google Vertex AI, Ollama
```

**Basic command pattern** (after controller is deployed):
```bash
kagent dashboard                                   # Open web UI
kagent "analyze cluster health in todo-app"        # Natural language query
kagent "diagnose CrashLoopBackOff in todo-app"     # Diagnostics
kagent "suggest HPA for backend at 60% CPU"        # Recommendations
```

**Note**: kagent requires the controller to be running in the cluster (deployed via
`kagent install`). The KUBECONFIG must point to Minikube. For Phase IV, run
`kagent install --profile demo` after Minikube starts and before Step 12.

**Alternatives Considered**:
- k8sgpt: Simpler standalone binary but less conversational and no built-in toolserver
  ecosystem; retained as fallback if kagent install fails in Minikube.
- kubectl-ai: Already in the toolchain for manifest generation; kagent is additive for
  cluster analysis and AIOps operations.

---

## R-006 — Minikube metrics-server Addon (for HPA)

**Decision**: Enable metrics-server addon before deploying HPA resources.

**Why required**: HorizontalPodAutoscaler requires the Kubernetes Metrics API
(`metrics.k8s.io/v1beta1`) to read CPU/memory utilisation. Without metrics-server,
`kubectl get hpa` shows `<unknown>` for current utilisation and HPA cannot scale.

**Enable**:
```bash
minikube addons enable metrics-server
minikube addons list | grep metrics-server   # Confirm enabled
```

**Verification** (wait ~60s after enabling):
```bash
kubectl top nodes
kubectl top pods -n todo-app   # Should show CPU/memory values
```

**HPA notes for Minikube**:
- Minikube single-node: HPA scaling will work but all pods land on the same node.
- If `kubectl top` returns "Metrics not yet available": wait 60–90 s and retry.

---

## R-007 — Helm Chart Best Practices for Local Minikube (2-service, NodePort)

**Decision**: Single chart with both services as templates; `values-local.yaml` overrides
for Minikube-specific settings.

**Chart structure**:
```
helm/todo-chatbot/
├── Chart.yaml          # name: todo-chatbot, version: 0.1.0, appVersion: v1
├── values.yaml         # production defaults (ClusterIP, standard resources)
├── values-local.yaml   # Minikube overrides
└── templates/
    ├── _helpers.tpl
    ├── frontend-deployment.yaml
    ├── frontend-service.yaml
    ├── backend-deployment.yaml
    └── backend-service.yaml
```

**values.yaml defaults** (production-oriented):
```yaml
frontend:
  image: todo-frontend
  tag: v1
  replicas: 2
  service:
    type: ClusterIP
    port: 80
    targetPort: 3000

backend:
  image: todo-backend
  tag: v1
  replicas: 1
  service:
    type: ClusterIP
    port: 8000
    targetPort: 8000

resources:
  frontend:
    requests: { cpu: "100m", memory: "128Mi" }
    limits:   { cpu: "200m", memory: "256Mi" }
  backend:
    requests: { cpu: "100m", memory: "128Mi" }
    limits:   { cpu: "300m", memory: "256Mi" }
```

**values-local.yaml overrides** (Minikube):
```yaml
frontend:
  service:
    type: NodePort
  imagePullPolicy: Never

backend:
  imagePullPolicy: Never

resources:
  frontend:
    requests: { cpu: "50m",  memory: "64Mi" }
    limits:   { cpu: "200m", memory: "256Mi" }
  backend:
    requests: { cpu: "50m",  memory: "64Mi" }
    limits:   { cpu: "200m", memory: "256Mi" }
```

**Helm install command**:
```bash
helm install todo ./helm/todo-chatbot \
  --namespace todo-app \
  --values ./helm/todo-chatbot/values-local.yaml \
  --wait --timeout 120s
```

---

## R-008 — Resource Requests/Limits for Minikube (2 CPU, 4–8 GB RAM)

**Decision**: Conservative starting values; reduce further if OOMKilled.

| Service | CPU Request | CPU Limit | Memory Request | Memory Limit |
|---------|------------|-----------|----------------|--------------|
| frontend (×2) | 50m | 200m | 64Mi | 256Mi |
| backend (×1) | 50m | 200m | 64Mi | 256Mi |
| **Total (all pods)** | **150m** | **600m** | **192Mi** | **768Mi** |

**Rationale**: A single Minikube node with 4 GB RAM and 2 CPUs (2000m) must also run
Minikube system components (~500m CPU, ~500Mi RAM). The above totals leave ~1850m CPU and
~3.5GB RAM available for system + other workloads. This is safe headroom.

**Scaling guidance**: If backend needs more capacity, increase replicas via HPA or manually.

---

## Resolved Unknowns Summary

| ID | Unknown | Resolution |
|----|---------|-----------|
| R-001 | Frontend base image | node:18-alpine, standalone output mode |
| R-002 | Backend base image | python:3.11-slim, uvicorn CMD |
| R-003 | Minikube image loading on Windows | minikube image load + imagePullPolicy: Never |
| R-004 | kubectl-ai install/config | go install GCP version + GEMINI_API_KEY or OPENAI_API_KEY |
| R-005 | kagent install/config | go install + OPENAI_API_KEY |
| R-006 | metrics-server for HPA | minikube addons enable metrics-server |
| R-007 | Helm chart structure | Single chart, values-local.yaml overrides |
| R-008 | Resource limits for Minikube | CPU 50m req / 200m limit; Mem 64Mi req / 256Mi limit |

**All NEEDS CLARIFICATION items resolved. Phase 1 design can proceed.**
