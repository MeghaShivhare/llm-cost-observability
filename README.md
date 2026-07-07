# LLM Cost & Observability Stack

FinOps-style observability for LLM API usage: cost, tokens, latency, and error
rate tracked per model tier and visualized in Grafana — the same
Prometheus/Grafana playbook used for infra cost monitoring, applied to LLM
spend instead of cloud spend.

## Stack

- **mock-llm** — a minimal OpenAI-compatible chat completions endpoint
  (stands in for a real provider so the stack runs with zero API keys/cost)
- **LiteLLM proxy** — routes requests, computes per-request cost from
  configured per-token pricing, and exports Prometheus metrics
- **Prometheus** — scrapes LiteLLM's `/metrics` endpoint
- **Grafana** — dashboards for spend, tokens, latency, and errors

Two model tiers (`mini-model`, `flagship-model`) point at the same mock
backend but carry different configured per-token pricing, so the dashboard
shows a real cost-by-tier breakdown — mirroring how you'd track spend across
cheap vs. flagship models in production.

## Run it

```bash
docker-compose up -d --build
./generate_traffic.sh 100   # fire sample requests across both tiers
```

Open Grafana at http://localhost:3000 (anonymous admin access enabled for
local demo purposes) — the "LLM Cost & Observability" dashboard is
pre-provisioned.

## Dashboard panels

- Total spend, total requests, total tokens, p95 API latency
- Spend by model tier (time series)
- Input/output tokens by model tier (time series)
- Request rate by HTTP status code
- Deployment-level failures (upstream errors retried by LiteLLM)

## Why

Most LLMOps cost content comes from ML engineers. This is the infra/DevOps
angle: the same cost-attribution and observability approach used for cloud
spend, pointed at LLM API spend instead.
