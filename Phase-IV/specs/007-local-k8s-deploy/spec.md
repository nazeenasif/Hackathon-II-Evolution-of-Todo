# Feature Specification: Phase IV – Local Kubernetes Deployment (Minikube + Agentic AI Tools)

**Feature Branch**: `007-local-k8s-deploy`
**Created**: 2026-02-13
**Status**: Draft
**Input**: User description: Cloud Native Todo Chatbot – Phase IV: Local Kubernetes Deployment using
Minikube + Agentic AI Tools

## User Scenarios & Testing *(mandatory)*

### User Story 1 – Environment Verified & Ready (Priority: P1)

A developer setting up Phase IV confirms that all required local tooling is installed, running,
and configured before any containerisation or deployment work begins. Every tool must respond to
a verification command and the Minikube cluster must be reachable.

**Why this priority**: Nothing else in Phase IV can proceed without a working local environment.
This is the gate that unlocks all subsequent stories.

**Independent Test**: Run each verification command in sequence; the story is complete when every
command exits successfully and Minikube is in the Running state.

**Acceptance Scenarios**:

1. **Given** a developer's workstation, **When** they run `docker version`, **Then** Docker
   Desktop ≥ 4.53 is reported and the Docker AI Agent (Gordon) toggle is confirmed enabled in
   Beta settings.
2. **Given** Docker Desktop running, **When** they run `minikube start --driver=docker`, **Then**
   Minikube starts a single-node cluster and `minikube status` shows `host: Running`, `kubelet:
   Running`, `apiserver: Running`.
3. **Given** Minikube running, **When** they run `helm version`, **Then** Helm 3+ is reported.
4. **Given** Helm available, **When** they run `kubectl-ai --version`, **Then** the GoogleCloudPlatform
   version of kubectl-ai is reported and an LLM provider key (GEMINI_API_KEY or OPENAI_API_KEY)
   is configured.
5. **Given** kubectl-ai configured, **When** they run `kagent version`, **Then** kagent CLI
   responds and an LLM provider is configured (OPENAI_API_KEY).
6. **Given** all tools verified, **When** they confirm the Phase III source code is present,
   **Then** separate `frontend/` and `backend/` directories exist and are non-empty.

---

### User Story 2 – Services Containerised with AI Assistance (Priority: P2)

A developer uses Gordon (Docker AI Agent) as the primary interface to analyse the application
source code and generate production-ready Dockerfiles for both the frontend and backend services.
If Gordon is unavailable, Claude Code is used as fallback to generate equivalent artefacts.

**Why this priority**: Container images are prerequisite to any Kubernetes deployment. This must
complete before the cluster deployment story.

**Independent Test**: Both `todo-frontend:v1` and `todo-backend:v1` images exist locally (or in
Minikube's image cache), and each service starts without errors when run locally with its expected
port exposed.

**Acceptance Scenarios**:

1. **Given** Gordon is available, **When** the developer runs
   `docker ai "Analyze my frontend code in ./frontend and generate an optimized Dockerfile"`,
   **Then** Gordon produces a valid Dockerfile saved to `frontend/Dockerfile`.
2. **Given** Gordon is available, **When** the developer runs
   `docker ai "Generate Dockerfile for backend in ./backend with multi-stage build"`,
   **Then** Gordon produces a valid multi-stage Dockerfile saved to `backend/Dockerfile`.
3. **Given** Gordon is unavailable/region-restricted, **When** Claude Code generates the
   Dockerfiles, **Then** both Dockerfiles exist, use non-root users, and build successfully.
4. **Given** both Dockerfiles exist, **When** images are built, **Then** `todo-frontend:v1` and
   `todo-backend:v1` images are present in the local Docker image list.
5. **Given** images built, **When** each image is run locally with its expected port, **Then**
   the health endpoint returns a successful response.
6. **Given** images verified locally, **When** they are loaded into Minikube
   (`minikube image load`), **Then** both images are accessible to the Minikube cluster without
   requiring a registry.
7. **Given** all steps complete, **When** the developer reviews the artefacts directory,
   **Then** all Gordon prompts, generated Dockerfiles, `.dockerignore` files, and build outputs
   are saved in `docs/phase-iv/containerisation/`.

---

### User Story 3 – Application Deployed to Minikube via kubectl-ai (Priority: P3)

A developer uses kubectl-ai to generate and apply Kubernetes manifests through natural language
prompts, deploying the frontend and backend into a dedicated `todo-app` namespace with health
probes, resource limits, and proper service exposure.

**Why this priority**: Core deployment is the central deliverable of Phase IV; all other stories
build on a running cluster state.

**Independent Test**: `kubectl get all -n todo-app` shows all Deployments available and all Pods
in Running/Ready state; the frontend is reachable via `minikube service todo-frontend --url`.

**Acceptance Scenarios**:

1. **Given** Minikube running and images loaded, **When** the developer runs
   `kubectl-ai "create namespace todo-app"`, **Then** the `todo-app` namespace exists.
2. **Given** namespace exists, **When** kubectl-ai generates and the developer applies a frontend
   Deployment manifest, **Then** the Deployment runs 2 replicas, each with an HTTP readiness
   probe on the container port, an HTTP liveness probe, CPU request ≤100m, and memory request
   ≤128Mi.
3. **Given** frontend deployed, **When** kubectl-ai generates and the developer applies a backend
   Deployment manifest, **Then** the Deployment runs at least 1 replica with equivalent probes
   and resource constraints.
4. **Given** both Deployments exist, **When** services are created via kubectl-ai, **Then** the
   backend has a ClusterIP service and the frontend has a NodePort service.
5. **Given** services created, **When** the developer retrieves the frontend URL via
   `minikube service todo-frontend --url`, **Then** the URL loads the Todo application UI.
6. **Given** deployment complete, **When** all kubectl-ai prompts, generated YAML files, and
   apply outputs are reviewed, **Then** all artefacts are saved in
   `docs/phase-iv/kubernetes-manifests/`.

---

### User Story 4 – Deployment Packaged as Helm Chart (Priority: P4)

A developer uses kubectl-ai or Claude Code to generate a complete Helm chart (`todo-chatbot`
v0.1.0) that encapsulates the frontend and backend Deployments, Services, and health probe
configuration, and installs it into Minikube using a Minikube-specific values override file.

**Why this priority**: Helm packaging provides reproducible, version-controlled deployments and
is an explicit Phase IV deliverable.

**Independent Test**: `helm list -n todo-app` shows the `todo` release with status `deployed`;
the application is end-to-end functional after a clean `helm install` from the generated chart.

**Acceptance Scenarios**:

1. **Given** deployment manifests from US3 exist, **When** a Helm chart is generated (via
   kubectl-ai or Claude Code), **Then** the chart directory contains `Chart.yaml`,
   `values.yaml`, and `templates/` with Deployment and Service templates for both services.
2. **Given** the chart exists, **When** `values-local.yaml` is created with Minikube-specific
   overrides (service type NodePort, reduced resource requests), **Then** the file correctly
   overrides defaults without modifying the base `values.yaml`.
3. **Given** the chart and override file exist, **When** the developer runs
   `helm install todo ./todo-chatbot -n todo-app --values values-local.yaml`, **Then** the
   installation succeeds and all pods reach Running/Ready within 120 seconds.
4. **Given** the chart is installed, **When** the developer runs
   `helm upgrade todo ./todo-chatbot -n todo-app --values values-local.yaml` after a values
   change, **Then** the upgrade applies without downtime.
5. **Given** an upgrade, **When** the developer runs `helm rollback todo -n todo-app`, **Then**
   the previous revision is restored successfully.
6. **Given** Helm operations complete, **When** the developer reviews the artefacts directory,
   **Then** the full chart source and all helm command outputs are saved in
   `docs/phase-iv/helm-chart/`.

---

### User Story 5 – Cluster Analysed and Optimised with kagent (Priority: P5)

A developer uses kagent to analyse the running cluster, diagnose any issues, and receive
optimisation recommendations for resource usage and autoscaling. Fixes are applied iteratively
using kubectl-ai based on kagent's findings.

**Why this priority**: AIOps validation is an explicit Phase IV deliverable and demonstrates
intelligent cluster management beyond basic deployment.

**Independent Test**: kagent completes a health analysis of the `todo-app` namespace with no
critical findings; at least one resource optimisation or autoscaling recommendation is documented
and applied.

**Acceptance Scenarios**:

1. **Given** the application is deployed and running, **When** the developer runs
   `kagent "analyze cluster health in todo-app namespace"`, **Then** kagent returns a health
   report covering pod status, resource utilisation, and any warnings.
2. **Given** any pod errors exist, **When** the developer runs
   `kagent "diagnose why any pods are in CrashLoopBackOff or Pending"`, **Then** kagent
   identifies the root cause and suggests remediation steps.
3. **Given** kagent's resource analysis, **When** kubectl-ai applies the recommended resource
   adjustments, **Then** updated Deployments show optimised resource requests/limits and all
   pods remain healthy.
4. **Given** the backend is running, **When** kagent recommends a HorizontalPodAutoscaler,
   **Then** the developer documents the recommendation and applies it if CPU metrics are
   available.
5. **Given** all kagent sessions complete, **When** the developer reviews the artefacts
   directory, **Then** all kagent queries, outputs, and applied fixes are saved in
   `docs/phase-iv/aiops/`.

---

### Edge Cases

- What happens when Gordon is unavailable due to region/tier restrictions? → Claude Code
  generates all Dockerfiles and build commands as documented fallback.
- What happens when Minikube cannot pull the image (ImagePullBackOff)? → Images are loaded
  directly via `minikube image load` to bypass registry requirements.
- What happens when a pod enters CrashLoopBackOff? → kagent diagnoses the cause; kubectl-ai
  generates a fix manifest; the fix is applied and verified.
- What happens when resource requests exceed Minikube node capacity (single-node)? → Reduce
  replicas to 1 and lower resource requests using `values-local.yaml` overrides.
- What happens when kubectl-ai generates invalid YAML? → The generated file is reviewed and
  corrected via Claude Code before applying; both the original and corrected versions are saved.
- What happens when a Helm install fails mid-way? → Run `helm uninstall todo -n todo-app` to
  clean up, fix the issue, and reinstall from scratch.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The deployment environment MUST include Docker Desktop ≥ 4.53 with Gordon
  (Docker AI Agent) enabled, Minikube (Docker driver), Helm 3+, kubectl-ai (GoogleCloudPlatform
  version), and kagent — all verified before any implementation task begins.
- **FR-002**: All frontend and backend container images MUST be generated using Gordon as the
  primary tool, with Claude Code as the explicit fallback when Gordon is unavailable.
- **FR-003**: Container images MUST use non-root users, minimal base images, and include
  `.dockerignore` files; multi-stage builds MUST be used for the backend.
- **FR-004**: Both `todo-frontend:v1` and `todo-backend:v1` images MUST be verified running
  locally before being loaded into Minikube.
- **FR-005**: All Kubernetes manifests MUST be generated via kubectl-ai natural language prompts;
  generated YAML MUST be saved to the `docs/phase-iv/kubernetes-manifests/` directory.
- **FR-006**: Frontend Deployment MUST run 2–3 replicas; backend MUST run 1–3 replicas with
  scaling potential.
- **FR-007**: Every Deployment MUST include HTTP readiness and liveness probes, and define
  resource requests (CPU and memory).
- **FR-008**: A Helm chart named `todo-chatbot` version 0.1.0 MUST be generated covering both
  services, with a `values-local.yaml` Minikube override file.
- **FR-009**: The Helm chart MUST support install, upgrade, and rollback operations without data
  loss.
- **FR-010**: kagent MUST be used post-deployment to perform cluster health analysis, pod
  diagnostics, and resource optimisation; findings MUST be documented.
- **FR-011**: At least 80% of all DevOps operations MUST be performed via AI tools (Gordon,
  kubectl-ai, kagent); the ratio MUST be calculable from the saved prompt log.
- **FR-012**: Every AI prompt, generated artefact (Dockerfile, manifest, chart), command
  executed, and output/error MUST be saved in the `docs/phase-iv/` directory structure.

### Key Entities

- **Container Image**: A versioned, tagged Docker image for a service (frontend or backend);
  attributes: name, tag, base image, build stage count, non-root user flag.
- **Kubernetes Deployment**: A declarative workload definition for a service; attributes:
  replicas, container image, resource requests/limits, readiness probe, liveness probe,
  namespace.
- **Kubernetes Service**: A network endpoint exposing a Deployment; attributes: type
  (ClusterIP or NodePort), port, targetPort, namespace.
- **Helm Chart**: A versioned package of Kubernetes templates; attributes: chart name, version,
  values.yaml (defaults), values-local.yaml (Minikube overrides), templates directory.
- **AI Tool Interaction Log**: A record of a single AI tool exchange; attributes: tool name,
  prompt text, generated artefact or output, timestamp, pass/fail outcome.
- **Namespace**: The Kubernetes namespace isolating all Phase IV resources; fixed value:
  `todo-app`.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All pods in the `todo-app` namespace reach Running/Ready state within 120 seconds
  of deployment, with zero restarts at steady state.
- **SC-002**: The frontend is accessible via a local URL and the complete Todo application
  (create, read, update, delete tasks) works end-to-end through the browser.
- **SC-003**: Zero critical Kubernetes error states (CrashLoopBackOff, ImagePullBackOff,
  OOMKilled, Pending > 5 min) exist in the final deployment.
- **SC-004**: At least 80% of all DevOps operations are performed via AI tools (Gordon,
  kubectl-ai, kagent), verified by counting prompts in the saved interaction log.
- **SC-005**: The entire deployment is reproducible from the saved `docs/phase-iv/` directory
  alone — a reviewer following only the logged prompts and commands can recreate the running
  cluster.
- **SC-006**: A Helm chart installs cleanly and produces an equivalent running state to the
  manually applied manifests; upgrade and rollback complete without service interruption.
- **SC-007**: kagent produces at least one cluster health report and one resource optimisation
  recommendation, both saved in `docs/phase-iv/aiops/`.

---

## Assumptions

- The Phase III Todo Chatbot source code (frontend and backend) is available and working locally
  before Phase IV begins.
- The backend service exposes an HTTP health endpoint; if not, a `/` route returning HTTP 200
  is used for probes.
- The frontend is built as a standard web application (React/Next.js) served on port 3000.
- The backend runs on port 8000 (FastAPI); if it differs, manifests are adjusted accordingly.
- A valid LLM provider API key (GEMINI or OPENAI) is available for configuring kubectl-ai and
  kagent before implementation begins.
- Minikube is configured with sufficient resources (≥2 CPUs, ≥4GB RAM) to run both services.
- Network connectivity is available during tool installation; all runtime operations are local.
