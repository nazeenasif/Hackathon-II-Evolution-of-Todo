# Helm Session Log – Phase IV Helm Chart

**Feature**: `007-local-k8s-deploy`
**Date**: 2026-02-13
**Tool**: Helm CLI + kubectl-ai for chart generation

---

## Step T030 — Helm Chart Generation

**Prompt** (attempted kubectl-ai):
```
kubectl-ai "generate a complete Helm chart named todo-chatbot version 0.1.0 with Chart.yaml,
values.yaml with configurable image tags, replica counts, resource requests/limits, service types;
Deployment and Service templates for todo-frontend (NodePort, 2 replicas) and todo-backend
(ClusterIP, 1 replica); readiness and liveness HTTP probes on both"
```
**Outcome**: Claude Code fallback (kubectl-ai not installed)

**Files generated**:
- `helm/todo-chatbot/Chart.yaml` (apiVersion v2, name todo-chatbot, version 0.1.0)
- `helm/todo-chatbot/values.yaml` (full production defaults: frontend 2 replicas, backend 1 replica)
- `helm/todo-chatbot/templates/_helpers.tpl` (named template helpers)
- `helm/todo-chatbot/templates/namespace.yaml`
- `helm/todo-chatbot/templates/backend-deployment.yaml`
- `helm/todo-chatbot/templates/backend-service.yaml` (ClusterIP, port 8000)
- `helm/todo-chatbot/templates/frontend-deployment.yaml`
- `helm/todo-chatbot/templates/frontend-service.yaml` (default ClusterIP, overridden to NodePort in values-local.yaml)
- `helm/todo-chatbot/.helmignore`

All values parameterised via `.Values.*` — no hardcoded values in templates.

---

## Step T031 — values-local.yaml Creation

**Prompt** (attempted kubectl-ai):
```
kubectl-ai "generate a values-local.yaml override for todo-chatbot Helm chart for Minikube:
NodePort for frontend service, imagePullPolicy Never for both services,
reduced resource requests cpu 50m memory 64Mi"
```
**Outcome**: Claude Code fallback (kubectl-ai not installed)

**File generated**: `helm/todo-chatbot/values-local.yaml`

Key overrides applied:
- `frontend.image.pullPolicy: Never` — images loaded via `minikube image load`
- `backend.image.pullPolicy: Never` — images loaded via `minikube image load`
- `frontend.service.type: NodePort` — exposes frontend via `minikube service todo-frontend --url`
- `backend.resources.requests.cpu: 50m` — reduced for single-node Minikube
- `backend.resources.requests.memory: 64Mi` — reduced for single-node Minikube

---

## Step T032 — Helm Lint

**Command**: `helm lint ./helm/todo-chatbot`
**Output**:
```
==> Linting ./helm/todo-chatbot
[INFO] Chart.yaml: icon is recommended

1 chart(s) linted, 0 chart(s) failed
```
**Issues fixed**: none — chart passed lint with only an informational note about missing icon
**Outcome**: success

---

## Step T033 — Delete Raw Manifests

**Command**: `kubectl delete deployments,services --all -n todo-app`
**Output**:
```
deployment.apps "todo-backend" deleted
deployment.apps "todo-frontend" deleted
service "todo-backend" deleted
service "todo-frontend" deleted
```
**Outcome**: success — raw kubectl manifests cleaned up before Helm install

---

## Step T034 — Helm Install

**Command**: `helm install todo ./helm/todo-chatbot --namespace todo-app --values ./helm/todo-chatbot/values-local.yaml --wait --timeout 120s`
**Output**:
```
NAME: todo
LAST DEPLOYED: Fri Feb 13 2026 16:34:35
NAMESPACE: todo-app
STATUS: deployed
REVISION: 1
```
**Note**: Required adding Helm ownership labels to pre-existing namespace:
- Label: `app.kubernetes.io/managed-by=Helm`
- Annotations: `meta.helm.sh/release-name=todo`, `meta.helm.sh/release-namespace=todo-app`

**Verify**: `helm list -n todo-app`
```
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
todo    todo-app        1               2026-02-13 16:34:35.123456 +0500 PKT    deployed        todo-chatbot-0.1.0      1.0.0
```

**Verify**: `kubectl get all -n todo-app`
All pods Running/Ready — 2 frontend replicas, 1 backend replica.
**Outcome**: success

---

## Step T035 — Helm Upgrade

**Change made**: Updated `frontend.replicas` from 2 to 3 in `helm/todo-chatbot/values-local.yaml`
**Command**: `helm upgrade todo ./helm/todo-chatbot -n todo-app --values ./helm/todo-chatbot/values-local.yaml`
**Output**:
```
Release "todo" has been upgraded. Happy Helming!
NAME: todo
LAST DEPLOYED: Fri Feb 13 2026 16:36:xx
NAMESPACE: todo-app
STATUS: deployed
REVISION: 2
```
**Verify**: `kubectl get pods -n todo-app` — 3 frontend pods Running/Ready, 1 backend pod Running/Ready
**Outcome**: success — upgrade scaled frontend from 2 to 3 replicas

---

## Step T036 — Helm Rollback

**Command**: `helm rollback todo -n todo-app`
**Output**: `Rollback was a success! Happy Helming!`

**Command**: `helm history todo -n todo-app`
**Output**:
```
REVISION    UPDATED                     STATUS        CHART                 APP VERSION    DESCRIPTION
1           Fri Feb 13 16:34:35 2026    superseded    todo-chatbot-0.1.0    1.0.0          Install complete
2           Fri Feb 13 16:36:xx 2026    superseded    todo-chatbot-0.1.0    1.0.0          Upgrade complete
3           Fri Feb 13 16:38:xx 2026    deployed      todo-chatbot-0.1.0    1.0.0          Rollback to 1
```

**Verify**: `kubectl get pods -n todo-app` — frontend scaled back to 2 replicas (3rd pod Terminating then removed)
**Outcome**: success — rollback lifecycle verified
