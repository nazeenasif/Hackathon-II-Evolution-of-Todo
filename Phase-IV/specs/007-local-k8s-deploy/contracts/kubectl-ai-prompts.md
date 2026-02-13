# Contracts: kubectl-ai Prompt → Expected YAML Output

**Feature**: `007-local-k8s-deploy`
**Date**: 2026-02-13
**Purpose**: Define the natural language prompts for kubectl-ai and their expected YAML output
contracts. These serve as the "API contract" between human intent and AI-generated K8s resources.

---

## Contract 1: Namespace Creation

**Prompt**:
```
kubectl-ai "create a namespace called todo-app in my Minikube cluster"
```

**Expected Output** (YAML):
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: todo-app
  labels:
    project: todo-chatbot
```

**Validation**:
- `kubectl get namespace todo-app` → STATUS: Active
- No errors in `kubectl describe namespace todo-app`

---

## Contract 2: Backend Deployment

**Prompt**:
```
kubectl-ai "create a Deployment named todo-backend in namespace todo-app using image
todo-backend:v1 with imagePullPolicy Never. Set 1 replica. Add readiness probe HTTP GET
/health port 8000 initialDelaySeconds 10. Add liveness probe HTTP GET /health port 8000
initialDelaySeconds 15. Set resource requests cpu 100m memory 128Mi and limits cpu 300m
memory 256Mi."
```

**Expected Output** (YAML):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
  namespace: todo-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: todo-backend
  template:
    metadata:
      labels:
        app: todo-backend
    spec:
      containers:
        - name: todo-backend
          image: todo-backend:v1
          imagePullPolicy: Never
          ports:
            - containerPort: 8000
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 10
            failureThreshold: 3
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 15
            periodSeconds: 20
            failureThreshold: 3
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "300m"
              memory: "256Mi"
```

**Validation**:
- `kubectl get deployment todo-backend -n todo-app` → READY: 1/1
- `kubectl rollout status deployment/todo-backend -n todo-app`

---

## Contract 3: Backend ClusterIP Service

**Prompt**:
```
kubectl-ai "create a ClusterIP Service named todo-backend in namespace todo-app.
Port 8000 targeting port 8000 on pods with app=todo-backend selector."
```

**Expected Output** (YAML):
```yaml
apiVersion: v1
kind: Service
metadata:
  name: todo-backend
  namespace: todo-app
spec:
  type: ClusterIP
  selector:
    app: todo-backend
  ports:
    - port: 8000
      targetPort: 8000
      protocol: TCP
```

**Validation**:
- `kubectl get service todo-backend -n todo-app` → TYPE: ClusterIP
- From frontend pod: `curl http://todo-backend:8000/health`

---

## Contract 4: Frontend Deployment

**Prompt**:
```
kubectl-ai "create a Deployment named todo-frontend in namespace todo-app using image
todo-frontend:v1 with imagePullPolicy Never. Set 2 replicas. Add readiness probe HTTP GET
/ port 3000 initialDelaySeconds 15. Add liveness probe HTTP GET / port 3000
initialDelaySeconds 20. Set resource requests cpu 100m memory 128Mi and limits cpu 200m
memory 256Mi. Add env var NEXT_PUBLIC_API_URL pointing to http://todo-backend:8000"
```

**Expected Output** (YAML):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-frontend
  namespace: todo-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: todo-frontend
  template:
    metadata:
      labels:
        app: todo-frontend
    spec:
      containers:
        - name: todo-frontend
          image: todo-frontend:v1
          imagePullPolicy: Never
          ports:
            - containerPort: 3000
          env:
            - name: NEXT_PUBLIC_API_URL
              value: "http://todo-backend:8000"
          readinessProbe:
            httpGet:
              path: /
              port: 3000
            initialDelaySeconds: 15
            periodSeconds: 10
            failureThreshold: 3
          livenessProbe:
            httpGet:
              path: /
              port: 3000
            initialDelaySeconds: 20
            periodSeconds: 20
            failureThreshold: 3
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "200m"
              memory: "256Mi"
```

**Validation**:
- `kubectl get deployment todo-frontend -n todo-app` → READY: 2/2

---

## Contract 5: Frontend NodePort Service

**Prompt**:
```
kubectl-ai "create a NodePort Service named todo-frontend in namespace todo-app.
Port 80 targeting port 3000 on pods with app=todo-frontend selector."
```

**Expected Output** (YAML):
```yaml
apiVersion: v1
kind: Service
metadata:
  name: todo-frontend
  namespace: todo-app
spec:
  type: NodePort
  selector:
    app: todo-frontend
  ports:
    - port: 80
      targetPort: 3000
      protocol: TCP
```

**Validation**:
- `kubectl get service todo-frontend -n todo-app` → TYPE: NodePort
- `minikube service todo-frontend --url` → returns accessible URL

---

## Contract 6: HorizontalPodAutoscaler

**Prompt**:
```
kubectl-ai "create a HorizontalPodAutoscaler for todo-backend in todo-app namespace.
Min 1 replica, max 3 replicas, target CPU utilisation 60%. Apply it."
```

**Expected Output** (YAML):
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: todo-backend-hpa
  namespace: todo-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: todo-backend
  minReplicas: 1
  maxReplicas: 3
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 60
```

**Validation** (requires metrics-server):
- `kubectl get hpa todo-backend-hpa -n todo-app`
- TARGETS column should show `X%/60%` (not `<unknown>/60%`)

---

## Contract 7: Helm Chart Structure Specification

**Prompt** (for kubectl-ai or Claude Code):
```
kubectl-ai "generate a complete Helm chart named todo-chatbot version 0.1.0 with the
following: Chart.yaml, values.yaml with configurable image tags, replica counts,
resource requests/limits, service types. Include Deployment and Service templates
for todo-frontend (NodePort, 2 replicas) and todo-backend (ClusterIP, 1 replica).
Add readiness and liveness HTTP probes to both Deployments."
```

**Expected Chart.yaml**:
```yaml
apiVersion: v2
name: todo-chatbot
description: A Helm chart for the Cloud Native Todo Chatbot (Phase IV)
type: application
version: 0.1.0
appVersion: "v1"
```

**Expected values.yaml** (production defaults):
```yaml
frontend:
  name: todo-frontend
  image: todo-frontend
  tag: v1
  replicas: 2
  imagePullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 80
    targetPort: 3000
  resources:
    requests:
      cpu: "100m"
      memory: "128Mi"
    limits:
      cpu: "200m"
      memory: "256Mi"

backend:
  name: todo-backend
  image: todo-backend
  tag: v1
  replicas: 1
  imagePullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 8000
    targetPort: 8000
  resources:
    requests:
      cpu: "100m"
      memory: "128Mi"
    limits:
      cpu: "300m"
      memory: "256Mi"

config:
  backendApiUrl: "http://todo-backend:8000"
```

**Expected values-local.yaml** (Minikube overrides):
```yaml
frontend:
  imagePullPolicy: Never
  service:
    type: NodePort
  resources:
    requests:
      cpu: "50m"
      memory: "64Mi"

backend:
  imagePullPolicy: Never
  resources:
    requests:
      cpu: "50m"
      memory: "64Mi"
```

**Validation**:
- `helm lint ./helm/todo-chatbot` → 0 errors, 0 warnings
- `helm install todo ./helm/todo-chatbot -n todo-app --values ./helm/todo-chatbot/values-local.yaml --dry-run` → no errors
