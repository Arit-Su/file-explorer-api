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
<pre> <code>
.
├── app/
│ ├── main.py
│ └── storage/ # Local and S3 backend logic
├── helm/file-explorer/ # Helm chart
├── Dockerfile
├── values.yaml # Helm values
└── README.md

---

## Getting Started

1. Build Docker Image (for Minikube)


eval $(minikube docker-env)
docker build -t file-explorer-api:local .
2. Deploy with Helm
Local Backend
helm install file-api ./helm/file-explorer/ \
  --set config.backendType=local \
  --set persistence.enabled=true
S3/MinIO Backend:

helm upgrade file-api ./helm/file-explorer/ \
  --set config.backendType=s3 \
  --set persistence.enabled=false
Access the App
Port Forward

kubectl port-forward svc/file-api-file-explorer-svc 8080:80
Then open: http://localhost:8080

Monitoring with Grafana
Enable Monitoring

helm upgrade file-api ./helm/file-explorer/ \
  --set monitoring.enabled=true
Access Grafana

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

Collected by Prometheus 

Evidences
![460137390-c308747f-ba29-4ace-ba10-e92cb72c106f](https://github.com/user-attachments/assets/a7ba80eb-e820-411a-9890-052ee194f298)
https://github-production-user-asset-6210df.s3.amazonaws.com/109128799/460137739-fe6e3819-f460-489e-b1d7-a99473e5bb4e.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20250627%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250627T205224Z&X-Amz-Expires=300&X-Amz-Signature=b1526b658fdc2b6c4c801e87374224efbe3bc8f5e70b6e4f0b5348c3339d996d&X-Amz-SignedHeaders=host
![460137631-3131461b-8844-4bb6-806c-7904d80064ce](https://github.com/user-attachments/assets/7cf8499e-49ba-4b15-a89d-189b47c8c3f5)
![460137677-aacd3809-667b-460a-a298-2a606e429ec0](https://github.com/user-attachments/assets/5204f9e6-ba3e-4c0c-bac5-2ad85751eca5)

  
  ![image](https://github.com/user-attachments/assets/c308747f-ba29-4ace-ba10-e92cb72c106f)
  ![image](https://github.com/user-attachments/assets/fe6e3819-f460-489e-b1d7-a99473e5bb4e)
  ![image](https://github.com/user-attachments/assets/3131461b-8844-4bb6-806c-7904d80064ce)
  ![image](https://github.com/user-attachments/assets/aacd3809-667b-460a-a298-2a606e429ec0)




