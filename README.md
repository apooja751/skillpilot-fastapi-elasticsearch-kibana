# SkillPilot – FastAPI Logging with Elasticsearch, Logstash & Kibana

## 1. Project Overview

This project demonstrates how to collect, process, store, and visualize application logs using the ELK Stack (Elasticsearch, Logstash, and Kibana) with a FastAPI application.

The application generates structured JSON logs for HTTP requests and sends them to Logstash. Logstash processes the logs and forwards them to Elasticsearch, where they can be searched and visualized using Kibana.

## 2. Objectives

- Develop a REST API using FastAPI.
- Generate structured JSON application logs.
- Configure Docker and Docker Compose for deployment.
- Collect logs using Logstash.
- Store and search logs in Elasticsearch.
- Use Kibana to explore logs and create dashboards.
- Test API endpoints and verify log ingestion.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| FastAPI | REST API framework |
| Uvicorn | ASGI application server |
| Docker | Containerization |
| Docker Compose | Multi-container management |
| Logstash | Log collection and processing |
| Elasticsearch | Log storage and search |
| Kibana | Log exploration and visualization |
| Git and GitHub | Version control and project hosting |

## 4. System Architecture

```text
Client / curl
     |
     v
FastAPI Application
     |
     v
Structured JSON Logs
     |
     v
Logstash (TCP Port 5000)
     |
     v
Elasticsearch
     |
     v
Kibana Dashboard
```

### Data Flow

1. A client sends an HTTP request to FastAPI.
2. FastAPI processes the request and generates structured logs.
3. The application sends log events to Logstash over TCP.
4. Logstash parses the JSON events and processes their timestamps.
5. Logstash forwards the events to Elasticsearch.
6. Kibana can be used to search, filter, and visualize stored logs.

## 5. Project Structure

```text
skillpilot-fastapi-elasticsearch-kibana/
├── app/
│   └── main.py
├── logstash/
│   └── logstash.conf
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 6. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Returns the application welcome message |
| GET | `/health` | Checks application health |
| GET | `/items/{item_id}` | Returns an item identifier and success status |
| GET | `/error-demo` | Generates a demonstration error log and returns HTTP 500 |

## 7. Setup and Execution

### Prerequisites

- GitHub Codespaces or a computer with Docker installed
- Docker Compose
- Git
- A web browser

### Step 1: Clone the Repository

```bash
git clone https://github.com/apooja751/skillpilot-fastapi-elasticsearch-kibana.git
cd skillpilot-fastapi-elasticsearch-kibana
```

### Step 2: Start the Services

```bash
docker compose up -d --build
```

### Step 3: Check Container Status

```bash
docker compose ps
```

The project uses four services:

- FastAPI
- Logstash
- Elasticsearch
- Kibana

### Step 4: Test the FastAPI Application

Test the welcome endpoint:

```bash
curl http://localhost:8000/
```

Test the health endpoint:

```bash
curl http://localhost:8000/health
```

Test the item endpoint:

```bash
curl http://localhost:8000/items/101
```

Test the error logging endpoint:

```bash
curl -i http://localhost:8000/error-demo
```

The error demonstration endpoint is expected to return HTTP 500.

## 8. Logstash Configuration

Logstash receives JSON-formatted events through a TCP input on port `5000`.

The pipeline:

- Receives log events using the `json_lines` codec.
- Processes event timestamps.
- Sends events to the Elasticsearch index `skillpilot-fastapi-logs`.
- Prints processed events to standard output for debugging.

The configured Elasticsearch index is:

```text
skillpilot-fastapi-logs
```

In this Codespaces environment, the Logstash output uses the Docker gateway address `172.18.0.1:9200`, which was verified to work in the current environment. This address may differ in another Docker environment.

## 9. Verify Logs in Elasticsearch

Check the Elasticsearch service:

```bash
curl -s http://localhost:9200/
```

List available indices:

```bash
curl -s "http://localhost:9200/_cat/indices?v"
```

Search the stored log documents:

```bash
curl -s "http://localhost:9200/skillpilot-fastapi-logs/_search?pretty"
```

The project has successfully created the `skillpilot-fastapi-logs` index, and two documents were present during verification.

The number of documents will increase as additional requests are logged and indexed.

## 10. Access the Services

When running in GitHub Codespaces, open the **Ports** tab and use the forwarded URLs for these ports.

| Service | Port |
|---|---:|
| FastAPI | 8000 |
| Logstash TCP input | 5000 |
| Elasticsearch | 9200 |
| Kibana | 5601 |

Kibana is available through the forwarded URL for port `5601`.

### Kibana Data View

After Elasticsearch contains logs:

1. Open Kibana.
2. Navigate to **Stack Management → Data Views**.
3. Create a data view named `skillpilot-fastapi-logs`.
4. Set the index pattern to `skillpilot-fastapi-logs*`.
5. Select `@timestamp` as the time field when prompted.
6. Open Discover to explore the stored log events.

A dashboard can then be created with visualizations for log levels, request paths, HTTP status codes, and log volume over time.

## 11. Testing and Results

The following checks have been performed:

- FastAPI endpoints returned the expected responses.
- Docker containers were started successfully.
- The FastAPI container could connect to the Logstash TCP input through the Docker gateway.
- Logstash successfully connected to Elasticsearch through the configured gateway.
- The Logstash pipeline started and was reported as running.
- Elasticsearch created the `skillpilot-fastapi-logs` index.
- Two log documents were present in the index during verification.

Kibana data-view and dashboard completion should be documented after they have been configured and tested.

## 12. Troubleshooting

### Check Container Logs

```bash
docker compose logs --tail=100 fastapi
docker compose logs --tail=100 logstash
docker compose logs --tail=100 elasticsearch
docker compose logs --tail=100 kibana
```

### Restart Services

```bash
docker compose restart
```

### Rebuild the FastAPI Service

```bash
docker compose up -d --build fastapi
```

### Recreate Logstash After Configuration Changes

```bash
docker compose up -d --force-recreate logstash
```

### Validate Docker Compose Configuration

```bash
docker compose config -q
```

## 13. Important Notes

- The Docker gateway address used in the Logstash configuration is environment-specific.
- The current Elasticsearch configuration disables built-in security and is intended for a learning environment. Do not expose this configuration publicly without appropriate security controls.
- The Elasticsearch index may show a yellow health status because the single-node setup cannot allocate its default replica shard.
- The `/error-demo` endpoint intentionally returns HTTP 500 for testing and should not be exposed unnecessarily in production.
- Stop the services when they are no longer needed to reduce resource usage.

## 14. Stop the Services

```bash
docker compose down
```

This stops and removes the project containers and network. The named Elasticsearch data volume is retained.

To remove the Elasticsearch data volume as well, use the following command only if you intentionally want to delete the stored data:

```bash
docker compose down -v
```

## 15. Conclusion

This project demonstrates how FastAPI application logs can be collected through Logstash, stored in Elasticsearch, and explored using Kibana. It provides practical experience with API development, structured logging, Docker containerization, log processing, and centralized log management.

