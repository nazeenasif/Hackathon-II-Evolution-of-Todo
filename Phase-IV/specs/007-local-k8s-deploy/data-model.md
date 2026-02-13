# Data Model: Phase IV – Local Kubernetes Deployment

**Feature**: `007-local-k8s-deploy`
**Date**: 2026-02-13
**Note**: This feature deploys infrastructure resources rather than application data models.
Entities below represent Kubernetes objects, Helm chart values, and artefact records.

---

## Entity 1: ContainerImage

A tagged Docker image built from application source code and loaded into Minikube.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| name | string | Required; `todo-frontend` or `todo-backend` | Registry prefix omitted (local only) |
| tag | string | Required; `v1` initially | Semantic versioning recommended |
| baseImage | string | Required; non-root, minimal | `node:18-alpine` or `python:3.11-slim` |
| stageCount | int | ≥ 2 (multi-stage) | Separate build and runtime layers |
| nonRootUser | bool | Must be `true` | Enforced by Principle X |
| exposedPort | int | 3000 (frontend) / 8000 (backend) | Must match probe config |
| imagePullPolicy | enum | `Never` (Minikube) / `IfNotPresent` | `Never` prevents registry pull failures |

**State transitions**: `Source code → build → local image → loaded into Minikube cache`

---

## Entity 2: KubernetesDeployment

A K8s Deployment object managing replica sets for a service in the `todo-app` namespace.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| name | string | Required; `todo-frontend` or `todo-backend` | Matches app label selector |
| namespace | string | Fixed: `todo-app` | Created in Step 6 |
| image | ContainerImage | Required | References Entity 1 |
| replicas | int | Frontend: 2–3; Backend: 1–3 | Per spec FR-006 |
| cpuRequest | string | ≥ `50m` | Kubernetes resource quantity |
| cpuLimit | string | ≤ `300m` (backend), ≤ `200m` (frontend) | Prevents CPU starvation |
| memoryRequest | string | ≥ `64Mi` | Per R-008 research |
| memoryLimit | string | ≤ `256Mi` | Per R-008 research |
| readinessProbe | HTTPProbe | Required; initialDelaySeconds ≥ 10 | Blocks traffic until app ready |
| livenessProbe | HTTPProbe | Required; initialDelaySeconds ≥ 15 | Restarts crashed containers |

### Sub-entity: HTTPProbe

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| path | string | `/` (frontend) / `/health` (backend) | Backend must expose /health route |
| port | int | Matches containerPort | 3000 or 8000 |
| initialDelaySeconds | int | ≥ 10 | Time for app to start |
| periodSeconds | int | Default: 10 | How often to probe |
| failureThreshold | int | Default: 3 | Restarts after 3 consecutive failures |

---

## Entity 3: KubernetesService

A K8s Service that exposes a Deployment within the cluster or externally.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| name | string | Required; matches Deployment name | `todo-frontend` or `todo-backend` |
| namespace | string | Fixed: `todo-app` | |
| type | enum | `NodePort` (frontend) / `ClusterIP` (backend) | NodePort for Minikube external access |
| port | int | 80 (frontend) / 8000 (backend) | External port |
| targetPort | int | 3000 (frontend) / 8000 (backend) | Container port |
| selector | map | `app: <service-name>` | Must match Deployment pod template labels |
| nodePort | int | 30000–32767 (auto-assigned for NodePort) | Assigned by Minikube |

---

## Entity 4: KubernetesNamespace

The logical isolation boundary for all Phase IV resources.

| Field | Value | Notes |
|-------|-------|-------|
| name | `todo-app` | Fixed; created in Step 6 |
| labels | `project: todo-chatbot` | For resource filtering |

---

## Entity 5: ConfigMap

K8s ConfigMap holding non-sensitive backend configuration.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| name | `todo-backend-config` | Fixed | |
| namespace | `todo-app` | Fixed | |
| DATABASE_URL | string | Required; Neon connection string | Set from `.env`; must not be committed |
| ENVIRONMENT | string | `production` | Passed to backend container as env var |

**Security note**: DATABASE_URL should be a Kubernetes Secret, not a ConfigMap.
For Phase IV demonstration purposes, a ConfigMap is used; a Secret would be used in production.

---

## Entity 6: HelmChart

The versioned Helm chart package for the full application.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| name | `todo-chatbot` | Fixed | Chart.yaml name field |
| version | `0.1.0` | SemVer | Increment on chart changes |
| appVersion | `v1` | String | Matches image tags |
| releaseName | `todo` | Helm release name used in `helm install` | |
| namespace | `todo-app` | Deployment target namespace | |
| valuesFile | `values.yaml` | Default values | Production-oriented defaults |
| overrideFile | `values-local.yaml` | Minikube overrides | NodePort, low resources, imagePullPolicy Never |

### HelmChart.Values schema (key paths)

```yaml
frontend.image        # ContainerImage.name
frontend.tag          # ContainerImage.tag
frontend.replicas     # KubernetesDeployment.replicas
frontend.service.type # KubernetesService.type
backend.image         # ContainerImage.name
backend.tag           # ContainerImage.tag
backend.replicas      # KubernetesDeployment.replicas
resources.frontend.*  # CPU/memory request/limit values
resources.backend.*   # CPU/memory request/limit values
```

---

## Entity 7: AIToolInteractionLog

A record of a single AI tool exchange, required by FR-012 for reproducibility.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| tool | enum | `gordon` / `kubectl-ai` / `kagent` / `claude-code` | Which AI tool was invoked |
| prompt | string | Required; verbatim | Full natural language input |
| output | string | Required; verbatim | Generated artefact, YAML, or analysis text |
| artefactPath | string | Optional | Path where generated file was saved |
| timestamp | ISO-8601 | Required | When the interaction occurred |
| outcome | enum | `success` / `fallback` / `manual-correction` | For AI-ratio calculation |

**Grouping**: Logs are grouped into session files:
- `docs/phase-iv/containerisation/gordon-session.md`
- `docs/phase-iv/kubernetes-manifests/kubectl-ai-session.md`
- `docs/phase-iv/helm-chart/helm-session.md`
- `docs/phase-iv/aiops/kagent-session.md`

---

## Entity 8: HorizontalPodAutoscaler (HPA)

K8s HPA resource for dynamic backend scaling (Phase IV Step 13).

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| name | `todo-backend-hpa` | Fixed | |
| namespace | `todo-app` | Fixed | |
| targetDeployment | `todo-backend` | Fixed | References KubernetesDeployment |
| minReplicas | int | 1 | Minimum pods at all times |
| maxReplicas | int | 3 | Per spec FR-006 |
| cpuTargetUtilisation | int | 60% | Scale up when CPU > 60% |
| prerequisite | metrics-server addon | Must be enabled in Minikube | See R-006 |

---

## Relationships

```text
HelmChart
├── deploys → KubernetesDeployment (frontend)
│   ├── uses → ContainerImage (todo-frontend:v1)
│   ├── in → KubernetesNamespace (todo-app)
│   └── has → HTTPProbe (readiness + liveness)
├── deploys → KubernetesDeployment (backend)
│   ├── uses → ContainerImage (todo-backend:v1)
│   ├── in → KubernetesNamespace (todo-app)
│   ├── has → HTTPProbe (readiness + liveness)
│   └── configured by → ConfigMap (todo-backend-config)
├── creates → KubernetesService (todo-frontend, NodePort)
└── creates → KubernetesService (todo-backend, ClusterIP)

HorizontalPodAutoscaler
└── scales → KubernetesDeployment (backend)
    └── requires → metrics-server addon

AIToolInteractionLog
└── documents → all entities above (generated artefacts)
```
