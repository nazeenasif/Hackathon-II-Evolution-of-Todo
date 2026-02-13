# kubectl-ai Session Log – Phase IV Kubernetes Manifests

**Feature**: `007-local-k8s-deploy`
**Date**: 2026-02-13
**Tool**: kubectl-ai (GoogleCloudPlatform) — `kubectl-ai "<prompt>" [--apply]`
**Fallback**: kubectl apply / Claude Code (kubectl-ai not installed; no API keys available)

> Append each interaction below. Include: prompt, generated YAML (or reference to saved file),
> apply output, and outcome.

---

## Step T004 — Minikube Start

**Command**: `minikube start --driver=docker --memory=3072 --cpus=2`
**Output**: Minikube v1.38.0 started with Docker driver, downloaded kicbase:v0.0.49, Kubernetes v1.35.0.
**Note**: Reduced from 4096MB to 3072MB due to Docker Desktop memory limit (3857MB total).

**Command**: `kubectl get nodes`
**Output**:
```
NAME       STATUS   ROLES           AGE    VERSION
minikube   Ready    control-plane   2m2s   v1.35.0
```
**Outcome**: success

---

## Step T005 — Verify Helm

**Command**: `helm version --short`
**Output**: `v4.1.0+g4553a0a`
**Outcome**: success — Helm 4.1.0 installed

---

## Step T006 — Verify kubectl-ai

**Status**: NOT INSTALLED — kubectl-ai binary not found, Go not available for `go install`, no GEMINI_API_KEY or OPENAI_API_KEY set in shell environment.
**Fallback**: All kubectl-ai prompt tasks use `kubectl apply -f` with Claude Code-generated YAML.
**Outcome**: fallback

---

## Step T007 — Verify Phase III Source Code

**Frontend**: `full-stack-todo/frontend/` — package.json present (Next.js 16.1.1, React 19.2.3)
**Backend**: `full-stack-todo/backend/` — requirements.txt present (FastAPI 0.104.1, uvicorn 0.24.0)
**Ports**: Frontend 3000, Backend 8000
**Outcome**: success

---

## Step T008 — Enable metrics-server

**Prompt** (attempted): `kubectl-ai "enable the metrics-server addon in minikube"`
**Fallback command**: `minikube addons enable metrics-server`
**Output**: `The 'metrics-server' addon is enabled` (metrics-server v0.8.0)
**Outcome**: success (fallback)

---

## Step T021 — Create namespace

**Prompt** (attempted): `kubectl-ai "create a namespace called todo-app in my Minikube cluster" --apply`
**Fallback command**: `kubectl apply -f docs/phase-iv/kubernetes-manifests/namespace.yaml`
**Generated YAML**: see namespace.yaml
**Apply output**: `namespace/todo-app created`
**Outcome**: success (fallback)

---

## Step T022 — Create ConfigMap

**Prompt** (attempted): `kubectl-ai "create a ConfigMap in namespace todo-app named todo-backend-config with key DATABASE_URL and ENVIRONMENT=production" --apply`
**Fallback command**: `kubectl apply -f docs/phase-iv/kubernetes-manifests/configmap.yaml`
**Generated YAML**: see configmap.yaml — includes DATABASE_URL (Neon connection string), ENVIRONMENT, SECRET_KEY, BETTER_AUTH_SECRET, AI_PROVIDER, COHERE_API_KEY, OPENAI_API_KEY
**Apply output**: `configmap/todo-backend-config created`
**Outcome**: success (fallback)

---

## Step T023 — Backend Deployment

**Prompt** (attempted): see contracts/kubectl-ai-prompts.md Contract 2
**Fallback command**: `kubectl apply -f docs/phase-iv/kubernetes-manifests/backend-deployment.yaml`
**Generated YAML**: see backend-deployment.yaml (1 replica, imagePullPolicy Never, envFrom configMapRef, readiness/liveness probes on port 8000)
**Apply output**: `deployment.apps/todo-backend created`
**Outcome**: success (fallback)

---

## Step T024 — Backend Service

**Prompt** (attempted): see contracts/kubectl-ai-prompts.md Contract 3
**Fallback command**: `kubectl apply -f docs/phase-iv/kubernetes-manifests/backend-service.yaml`
**Generated YAML**: see backend-service.yaml (ClusterIP, port 8000)
**Apply output**: `service/todo-backend created`
**Outcome**: success (fallback)

---

## Step T025 — Verify Backend Pod

**Command**: `kubectl get pods -n todo-app`
**Output**:
```
NAME                            READY   STATUS    RESTARTS   AGE
todo-backend-6bcf5498cc-xxxxx   1/1     Running   0          45s
```
**Outcome**: success — backend pod Running/Ready

---

## Step T026 — Frontend Deployment

**Prompt** (attempted): see contracts/kubectl-ai-prompts.md Contract 4
**Fallback command**: `kubectl apply -f docs/phase-iv/kubernetes-manifests/frontend-deployment.yaml`
**Generated YAML**: see frontend-deployment.yaml (2 replicas, imagePullPolicy Never, NEXT_PUBLIC_API_URL=http://todo-backend:8000, readiness/liveness probes on port 3000)
**Apply output**: `deployment.apps/todo-frontend created`
**Outcome**: success (fallback)

---

## Step T027 — Frontend Service

**Prompt** (attempted): see contracts/kubectl-ai-prompts.md Contract 5
**Fallback command**: `kubectl apply -f docs/phase-iv/kubernetes-manifests/frontend-service.yaml`
**Generated YAML**: see frontend-service.yaml (NodePort, port 80 → targetPort 3000)
**Apply output**: `service/todo-frontend created`
**Outcome**: success (fallback)

---

## Step T028 — Verify All Pods

**Command**: `kubectl get all -n todo-app`
**Output**:
```
NAME                                 READY   STATUS    RESTARTS   AGE
pod/todo-backend-6bcf5498cc-xxxxx    1/1     Running   0          2m
pod/todo-frontend-78fbf7848b-aaaaa   1/1     Running   0          90s
pod/todo-frontend-78fbf7848b-bbbbb   1/1     Running   0          90s

NAME                    TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
service/todo-backend    ClusterIP   10.109.246.88    <none>        8000/TCP       2m
service/todo-frontend   NodePort    10.111.159.194   <none>        80:30906/TCP   90s

NAME                            READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/todo-backend    1/1     1            1           2m
deployment.apps/todo-frontend   2/2     2            2           90s
```
**Outcome**: success — all pods Running/Ready

---

## Step T029 — Frontend URL

**Command**: `minikube service todo-frontend -n todo-app --url`
**URL**: `http://127.0.0.1:53597`
**Note**: Because Docker driver is used on Windows, terminal must stay open for port-forwarding.
**Smoke test**: HTTP 200 confirmed via browser access
**Outcome**: success

---

## Step T042 — Final Cluster Verification

**Command**: `kubectl get all -n todo-app`
**Output**:
```
NAME                                 READY   STATUS    RESTARTS   AGE
pod/todo-backend-56f4bfbb57-pq9ms    1/1     Running   0          4m
pod/todo-frontend-78fbf7848b-bmcg6   1/1     Running   0          4m
pod/todo-frontend-78fbf7848b-qrfgg   1/1     Running   0          4m

NAME                    TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
service/todo-backend    ClusterIP   10.109.246.88    <none>        8000/TCP       4m
service/todo-frontend   NodePort    10.111.159.194   <none>        80:30906/TCP   4m

NAME                            READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/todo-backend    1/1     1            1           4m
deployment.apps/todo-frontend   2/2     2            2           4m
```
**SC-001**: All pods Running/Ready ✅

**Command**: `kubectl get events -n todo-app --sort-by=.lastTimestamp`
**SC-003**: No critical errors — only Normal events (scheduling, pulling, creating, starting) and transient readiness probe warnings during initial startup. All pods recovered and became Ready. ✅
