#!/usr/bin/env bash
# Fires a mix of requests across both model tiers so the dashboard has
# realistic cost, token, and latency data to show.
set -euo pipefail

LITELLM_URL="http://localhost:4000/chat/completions"
MASTER_KEY="sk-demo-master-key"
MODELS=("mini-model" "flagship-model")
PROMPTS=(
  "why is my nat gateway costing so much"
  "summarize this incident postmortem for me"
  "how do I right-size this EKS node group"
  "explain the root cause of the deployment rollback"
  "what's driving the AWS bill increase this month"
)

REQUESTS="${1:-60}"

for i in $(seq 1 "$REQUESTS"); do
  model=${MODELS[$((RANDOM % ${#MODELS[@]}))]}
  prompt=${PROMPTS[$((RANDOM % ${#PROMPTS[@]}))]}
  curl -s -o /dev/null -w "%{http_code} " -X POST "$LITELLM_URL" \
    -H "Authorization: Bearer $MASTER_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"model\":\"$model\",\"messages\":[{\"role\":\"user\",\"content\":\"$prompt\"}]}" &
  if (( i % 8 == 0 )); then wait; fi
done
wait
echo ""
echo "Sent $REQUESTS requests."
