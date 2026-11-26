# Kubernetes Observability Stack: Flask + Prometheus + Grafana

An end-to-end monitoring and visualization pipeline built on Kubernetes (k3s). A Python Flask application exposes custom Prometheus metrics at `/metrics`, which Prometheus scrapes every 15 seconds across cluster DNS and visualizes in real time using a custom Grafana dashboard.

## Architecture

```text
[ Flask App (:5000/metrics) ]  <--- scrapes (15s) ---  [ Prometheus (:9090) ]
     (default namespace)                                (monitoring namespace)
                                                                  ^
                                                                  | queries (PromQL)
                                                          [ Grafana (:3000) ]
                                                         (monitoring namespace)
```

## Tech Stack
* **Application:** Python, Flask, `prometheus-client`
* **Container & Orchestration:** Docker, Kubernetes (k3s)
* **Monitoring:** Prometheus
* **Visualization:** Grafana

## Project Structure

```text
.
├── app/                       # Flask application source code & Dockerfile
├── monitoring/
│   ├── configmap.yaml         # Prometheus scrape configuration
│   ├── prometheus.yaml        # Prometheus Deployment & ClusterIP Service
│   └── grafana.yaml           # Grafana Deployment, Service & datasource provisioning
├── flask-app.yaml             # Flask Deployment & Service
├── grafana-dashboard.json     # Exported Grafana dashboard panels
└── README.md
```

## Getting Started

### 1. Deploy the Flask Application
Deploy the Flask app and its ClusterIP service (`flask-metrics-service`) in the `default` namespace:
```bash
kubectl apply -f flask-app.yaml
```

### 2. Create the Monitoring Namespace & Deploy Stack
```bash
kubectl create namespace monitoring
kubectl apply -f monitoring/configmap.yaml
kubectl apply -f monitoring/prometheus.yaml
kubectl apply -f monitoring/grafana.yaml
```

### 3. Verify All Pods Are Running
```bash
kubectl get pods -n default
kubectl get pods -n monitoring
```

### 4. Access Grafana Locally
Forward the Grafana service port to your local machine:
```bash
kubectl port-forward svc/grafana-service -n monitoring 3000:3000
```
Open `http://localhost:3000` in your browser and log in with `admin` / `admin`.

### 5. Import the Dashboard
1. Go to **Dashboards → New → Import**.
2. Upload `grafana-dashboard.json`.
3. Select the **prometheus** data source and click **Import**.

### 6. Generate Sample Traffic
Port-forward the Flask service and hit a few routes (`/`, `/api`, `/health`) to see live metrics populate:
```bash
kubectl port-forward svc/flask-metrics-service -n default 5000:5000
```

## Dashboard Panels & PromQL Queries

* **Flask App Status:** `up{job="flask-app"}` — Live health status (`1` = Up, `0` = Down).
* **Flask App RAM (MB):** `process_resident_memory_bytes{job="flask-app"} / 1024 / 1024` — Real-time container memory footprint.
* **HTTP Request Rate:** `rate(http_requests_total[1m])` — Incoming requests per second across routes and status codes.
* **Total Requests by Endpoint:** `sum by (endpoint, method) (http_requests_total)` — Cumulative hits per route (`/`, `/api`, `/health`, `/metrics`).
* **Requests by HTTP Status Code:** `sum by (status) (http_requests_total)` — Breakdown of `200` vs `404` responses.
