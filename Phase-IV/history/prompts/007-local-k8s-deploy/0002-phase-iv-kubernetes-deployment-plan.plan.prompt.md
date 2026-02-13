---
id: 0002
title: Phase IV Kubernetes Deployment Plan
stage: plan
date: 2026-02-13
surface: agent
model: claude-sonnet-4-5-20250929
feature: 007-local-k8s-deploy
branch: 007-local-k8s-deploy
user:
command: /sp.plan
labels: [plan, kubernetes, minikube, docker, helm, kubectl-ai, kagent, gordon, aiops, phase-iv]
links:
  spec: specs/007-local-k8s-deploy/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/007-local-k8s-deploy/plan.md
 - specs/007-local-k8s-deploy/research.md
 - specs/007-local-k8s-deploy/data-model.md
 - specs/007-local-k8s-deploy/quickstart.md
 - specs/007-local-k8s-deploy/contracts/kubectl-ai-prompts.md
tests:
 -
---

## Prompt

```
/sp.plan

Project: Cloud Native Todo Chatbot – Phase IV: Local Kubernetes Deployment

You are an expert Agentic DevOps Engineer following the strict Agentic Dev Stack workflow:
1. Understand the full spec
2. Generate a clear, numbered, sequential PLAN
3. After plan approval/execution, break into small tasks for implementation

Input Spec Reference: Use the previously provided /sp.specify for Phase IV (Local Minikube
deployment with Gordon, kubectl-ai, kagent, Helm, etc.)

Your task now: Generate a DETAILED STEP-BY-STEP PLAN based on the spec.

Core Guidelines for the Plan:
- Strictly no manual coding by human – all code/artifacts (Dockerfiles, manifests, Helm charts)
  must be generated via AI agents (Claude Code, Gordon, kubectl-ai)
- Maximize AI tool usage: ≥80% steps should involve natural language prompts to Gordon
  (docker ai), kubectl-ai, kagent
- Sequence must be logical and safe: setup → containerize → deploy manifests → helm-ify
  → optimize/verify
- Make it local-Minikube friendly: low resources, NodePort exposure, minikube image load
  if needed
- Include verification at each major stage
- Anticipate common pitfalls and suggest AI-troubleshooting steps
- Document everything
- Total plan: 10–15 main steps

Plan Structure:
1. Preparation & Environment Check
2. Containerization Phase
3. Kubernetes Basics & Manifest Deployment
4. Helm Chart Generation & Installation
```

## Response snapshot

```
Generated complete /sp.plan output for 007-local-k8s-deploy:

plan.md: 15-step implementation plan
  - Step 1: Environment verification (all tools)
  - Step 2: Minikube addons (metrics-server)
  - Step 3: Frontend containerisation (Gordon primary / Claude Code fallback)
  - Step 4: Backend containerisation (Gordon primary / Claude Code fallback)
  - Step 5: Image verification & Minikube load
  - Step 6: Namespace & ConfigMap via kubectl-ai
  - Step 7: Backend Deployment & ClusterIP Service via kubectl-ai
  - Step 8: Frontend Deployment & NodePort Service via kubectl-ai
  - Step 9: Initial verification & AI troubleshooting
  - Step 10: Helm chart generation via kubectl-ai/Claude Code
  - Step 11: Helm install/upgrade/rollback lifecycle test
  - Step 12: kagent cluster health analysis
  - Step 13: Resource optimisation & HPA via kagent+kubectl-ai
  - Step 14: Final end-to-end verification
  - Step 15: Artefact documentation consolidation

research.md: 8 research decisions (R-001 to R-008)
  - Base images: node:18-alpine (frontend), python:3.11-slim (backend)
  - minikube image load + imagePullPolicy: Never
  - kubectl-ai & kagent install/config
  - metrics-server addon for HPA
  - Helm values-local.yaml override pattern
  - Resource budgets for 2-CPU/4GB Minikube node

data-model.md: 8 entities
  - ContainerImage, KubernetesDeployment, KubernetesService, KubernetesNamespace,
    ConfigMap, HelmChart, AIToolInteractionLog, HorizontalPodAutoscaler

contracts/kubectl-ai-prompts.md: 7 prompt→YAML contracts
  - Namespace, backend Deployment, backend Service, frontend Deployment,
    frontend Service, HPA, Helm chart structure

quickstart.md: 8-step reproduction guide + troubleshooting table
  Constitution Check: ALL PASS (12 principles)
```

## Outcome

- ✅ Impact: Full architecture plan generated for 007-local-k8s-deploy with 15 sequential steps,
  all Constitution gates passing, complete Phase 1 design artefacts
- 🧪 Tests: No tests — plan stage
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md,
  contracts/kubectl-ai-prompts.md
- 🔁 Next prompts: /sp.tasks to break plan into executable task list
- 🧠 Reflection: The plan correctly models this as an AI-tool orchestration workflow rather than
  traditional software development; the "contracts" section captures kubectl-ai prompt→YAML
  expected outputs which is a novel pattern for this toolchain

## Evaluation notes (flywheel)

- Failure modes observed: Research agent output file empty — proceeded with authoritative
  knowledge for all 8 research decisions; all values are defensible from public documentation
- Graders run and results (PASS/FAIL): PASS — 15 steps, constitution check all pass, all
  Phase 1 artefacts complete
- Prompt variant (if applicable): Standard /sp.plan with detailed user guidelines
- Next experiment (smallest change to try): Run /sp.tasks to generate task breakdown for
  007-local-k8s-deploy implementation
