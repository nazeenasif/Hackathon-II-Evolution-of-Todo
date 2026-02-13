# Quickstart: Phase IV – Local Kubernetes Deployment

**Feature**: `007-local-k8s-deploy`
**Date**: 2026-02-13
**Purpose**: Reproduction guide for a reviewer to recreate the full Phase IV deployment from
scratch using only this guide and the artefacts in `docs/phase-iv/`.

> **Prerequisites**: Windows workstation with internet connectivity for tool installation.
> All runtime operations are local (no cloud required).

---

## Step 0: Prerequisites — Install & Verify Tools

### 0a. Docker Desktop 4.53+

1. Download Docker Desktop ≥ 4.53 from [docker.com/products/docker-desktop](https://docker.com/products/docker-desktop)
2. Install and start Docker Desktop
3. In Docker Desktop → Settings → Beta Features → toggle **"Docker AI Agent (Gordon)"** ON
4. Verify: `docker version` → Server version 4.53+

### 0b. Minikube

```bash
# Windows (via winget):
winget install Kubernetes.minikube

# Or direct download from:
# https://storage.googleapis.com/minikube/releases/latest/minikube-installer.exe

minikube version   # Verify: v1.32+
```

### 0c. Helm 3

```bash
# Windows (via winget):
winget install Helm.Helm

helm version   # Verify: v3.14+
```

### 0d. kubectl-ai (GoogleCloudPlatform version)

```bash
# Requires Go 1.21+
go install github.com/GoogleCloudPlatform/kubectl-ai@latest

# Configure LLM provider (choose one):
export GEMINI_API_KEY="your-gemini-api-key"
# OR
export OPENAI_API_KEY="your-openai-api-key"

kubectl-ai --version   # Verify installation
```

### 0e. kagent

kagent is a Kubernetes-native controller; install the CLI first, then deploy the controller
into the cluster in Step 1.

```bash
# macOS/Linux/WSL2 (Homebrew):
brew install kagent

# Windows (direct binary from releases):
# https://github.com/kagent-dev/kagent/releases → download kagent.exe → add to PATH

# Configure LLM (required before kagent install):
export OPENAI_API_KEY="your-openai-api-key"

# Deploy controller into Minikube (run after minikube start in Step 1):
kagent install --profile demo

kagent version   # Verify CLI
```

### 0f. Verify Phase III Source Code

```bash
ls frontend/   # Must be non-empty Next.js project
ls backend/    # Must be non-empty FastAPI project
```

---

## Step 1: Start Minikube & Enable Addons

```bash
# Start cluster (allocate enough resources)
minikube start --driver=docker --memory=4096 --cpus=2

# Verify cluster
minikube status
kubectl get nodes   # Should show: minikube Ready

# Enable metrics-server (required for HPA later)
minikube addons enable metrics-server
```

---

## Step 2: Verify Gordon & Generate Frontend Dockerfile

```bash
# Verify Gordon
docker ai "What can you do?"
# → Save output to docs/phase-iv/containerisation/gordon-session.md

# Analyse and generate Dockerfile
docker ai "Analyze the Next.js application in ./frontend and generate an optimized multi-stage Dockerfile using node:18-alpine with standalone output mode, non-root user, expose port 3000"
# → Save generated Dockerfile to frontend/Dockerfile

docker ai "Generate a .dockerignore file for the Next.js project in ./frontend"
# → Save to frontend/.dockerignore

# Fallback (if Gordon unavailable):
# Use Claude Code: "Generate a production Next.js Dockerfile using node:18-alpine, multi-stage build, non-root user"
```

---

## Step 3: Generate Backend Dockerfile

```bash
docker ai "Generate an optimized multi-stage Dockerfile for the Python FastAPI backend in ./backend using python:3.11-slim, non-root user, expose port 8000, uvicorn startup"
# → Save generated Dockerfile to backend/Dockerfile

docker ai "Generate a .dockerignore for the Python project in ./backend"
# → Save to backend/.dockerignore

# Fallback (if Gordon unavailable):
# Use Claude Code: "Generate a production FastAPI Dockerfile using python:3.11-slim, multi-stage, non-root user"
```

---

## Step 4: Build & Verify Images Locally

```bash
# Build images
docker build -t todo-frontend:v1 ./frontend
docker build -t todo-backend:v1 ./backend

# Smoke test locally
docker run -d -p 3000:3000 --name fe-test todo-frontend:v1
curl http://localhost:3000   # Should return HTML
docker stop fe-test && docker rm fe-test

docker run -d -p 8000:8000 --name be-test todo-backend:v1
curl http://localhost:8000/health   # Should return {"status": "ok"}
docker stop be-test && docker rm be-test

# Load into Minikube
minikube image load todo-frontend:v1
minikube image load todo-backend:v1
minikube image ls | grep todo   # Verify both images listed
```

---

## Step 5: Deploy to Minikube via kubectl-ai

```bash
# Create namespace
kubectl-ai "create a namespace called todo-app"

# Deploy backend
kubectl-ai "create a Deployment named todo-backend in namespace todo-app using image todo-backend:v1 imagePullPolicy Never, 1 replica, HTTP readiness probe /health port 8000 initialDelay 10s, liveness probe /health port 8000 initialDelay 15s, CPU request 100m limit 300m, memory request 128Mi limit 256Mi" --apply
kubectl-ai "create a ClusterIP Service named todo-backend in namespace todo-app port 8000 targetPort 8000" --apply

# Deploy frontend
kubectl-ai "create a Deployment named todo-frontend in namespace todo-app using image todo-frontend:v1 imagePullPolicy Never, 2 replicas, HTTP readiness probe / port 3000 initialDelay 15s, liveness probe / port 3000 initialDelay 20s, CPU request 100m limit 200m, memory request 128Mi limit 256Mi, env NEXT_PUBLIC_API_URL=http://todo-backend:8000" --apply
kubectl-ai "create a NodePort Service named todo-frontend in namespace todo-app port 80 targetPort 3000" --apply

# Verify
kubectl get all -n todo-app
# Wait until all pods show READY 1/1 (or 2/2 for frontend)

# Get frontend URL
minikube service todo-frontend --url
# Open the URL in your browser
```

---

## Step 6: Package with Helm & Redeploy

```bash
# Generate Helm chart (via kubectl-ai or Claude Code)
kubectl-ai "generate a Helm chart named todo-chatbot v0.1.0 with frontend and backend Deployments and Services, configurable values for images, replicas, resources, service types"
# → Save chart to helm/todo-chatbot/
# → Create helm/todo-chatbot/values-local.yaml with imagePullPolicy: Never, NodePort for frontend

# Remove raw manifests from Step 5
kubectl delete deployments,services -n todo-app --all

# Install via Helm
helm install todo ./helm/todo-chatbot \
  --namespace todo-app \
  --values ./helm/todo-chatbot/values-local.yaml \
  --wait --timeout 120s

helm list -n todo-app           # Confirm: STATUS deployed
kubectl get all -n todo-app     # Confirm: all pods Running

# Test upgrade
helm upgrade todo ./helm/todo-chatbot -n todo-app --values ./helm/todo-chatbot/values-local.yaml

# Test rollback
helm rollback todo -n todo-app
helm history todo -n todo-app
```

---

## Step 7: AIOps with kagent

```bash
# Cluster health analysis
kagent "analyze the overall health of the todo-app namespace in Minikube. Report pod status, resource utilization, warnings."

# Resource optimisation
kagent "review the resource requests and limits for all deployments in todo-app and suggest optimized values for a single-node Minikube cluster"

# HPA recommendation
kagent "suggest a HorizontalPodAutoscaler for todo-backend that scales 1-3 replicas at 60% CPU"

# Apply HPA (if metrics-server available)
kubectl-ai "create a HorizontalPodAutoscaler for todo-backend in todo-app, min 1 max 3 replicas, CPU target 60%" --apply
kubectl get hpa -n todo-app
```

---

## Step 8: Final Verification

```bash
# All success criteria
kubectl get all -n todo-app                              # SC-001: all pods Running/Ready
minikube service todo-frontend --url                     # SC-002: get URL
# → Open URL, create/read/update/delete tasks           # SC-002: end-to-end CRUD works
kubectl get events -n todo-app --sort-by=.lastTimestamp  # SC-003: no critical errors
kubectl get hpa -n todo-app                              # HPA status

# Count AI tool operations (SC-004: ≥80%)
# Review session logs in docs/phase-iv/:
# - containerisation/gordon-session.md
# - kubernetes-manifests/kubectl-ai-session.md
# - helm-chart/helm-session.md
# - aiops/kagent-session.md
```

---

## Troubleshooting Reference

| Problem | Diagnosis | Fix |
|---------|-----------|-----|
| `ImagePullBackOff` | imagePullPolicy not set to Never | `kubectl-ai "update deployment to set imagePullPolicy Never in todo-app"` |
| `CrashLoopBackOff` | App crash or missing env vars | `kagent "diagnose why todo-backend is in CrashLoopBackOff"` |
| Probe failures (pod not Ready) | App not listening on expected port | Check Dockerfile EXPOSE and CMD; rebuild image |
| `<unknown>/60%` in HPA | metrics-server not ready | Wait 90s after enabling; `kubectl top nodes` |
| Minikube OOM | Too many replicas / high memory limits | Reduce replicas to 1 in values-local.yaml |
| Gordon unavailable | Region/tier restriction | Use Claude Code fallback; document in gordon-session.md |
| Neon DB connection refused | DATABASE_URL env var missing or wrong | Update ConfigMap `todo-backend-config`; redeploy backend |

---

## Artefact Directory Reference

```
docs/phase-iv/
├── containerisation/
│   ├── gordon-session.md        ← all docker ai prompts + outputs
│   ├── frontend/Dockerfile
│   ├── frontend/.dockerignore
│   ├── backend/Dockerfile
│   └── backend/.dockerignore
├── kubernetes-manifests/
│   ├── kubectl-ai-session.md    ← all kubectl-ai prompts + generated YAML
│   ├── namespace.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── backend-deployment.yaml
│   └── backend-service.yaml
├── helm-chart/
│   ├── helm-session.md          ← helm commands + outputs
│   └── todo-chatbot/            ← chart source
└── aiops/
    ├── kagent-session.md        ← kagent queries + outputs
    └── hpa-recommendation.yaml
```
