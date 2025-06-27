# File-Explorer-api

A FastAPI-based file explorer that supports browsing both local file systems and S3-compatible object storage (like MinIO). Easily deployable on Kubernetes with Helm.

---

## Features

-  Browse files and folders via REST API
-  Supports:
  - Local filesystem backend
  - S3/MinIO backend
-  Prometheus metrics endpoint for monitoring
-  Grafana dashboard support
-  Docker & Helm ready

---

## Project Structure

.
├── app/
│ ├── main.py
│ └── storage/ # Local and S3 backend logic
├── helm/file-explorer/ # Helm chart
├── Dockerfile
├── values.yaml # Helm values
└── README.md

yaml
Copy
Edit

---

## Getting Started

1. Build Docker Image (for Minikube)

```bash
eval $(minikube docker-env)
docker build -t file-explorer-api:local .
2. Deploy with Helm
Local Backend:
bash
Copy
Edit
helm install file-api ./helm/file-explorer/ \
  --set config.backendType=local \
  --set persistence.enabled=true
S3/MinIO Backend:
bash
Copy
Edit
helm upgrade file-api ./helm/file-explorer/ \
  --set config.backendType=s3 \
  --set persistence.enabled=false
Access the App
Port Forward
bash
Copy
Edit
kubectl port-forward svc/file-api-file-explorer-svc 8080:80
Then open: http://localhost:8080

Monitoring with Grafana
Enable Monitoring
bash
Copy
Edit
helm upgrade file-api ./helm/file-explorer/ \
  --set monitoring.enabled=true
Access Grafana
bash
Copy
Edit
kubectl get secret -n monitoring prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
Go to http://localhost:3000
Login with:

Username: admin

Password: 

View the fastapi-app dashboard under Dashboards → Browse.

API Endpoints
Method	Endpoint	Description
GET	/	List items at root directory
GET	/cloud-folder	List contents of a folder

Metrics
Available at: /metrics

Collected by Prometheus if monitoring is enabled
