import random
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

FAKE_REPLIES = [
    "Here's a summary of the incident: the root cause was a misconfigured autoscaler.",
    "Based on the logs, the failure originated in the payment service retry loop.",
    "The deployment succeeded, but latency increased 12% after the rollout.",
    "I'd recommend rightsizing the node group before enabling cluster autoscaling.",
    "The cost spike traces back to an idle NAT gateway left running over the weekend.",
]


@app.get("/v1/models")
def models():
    return {"data": [{"id": "demo-model", "object": "model"}]}


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()

    # simulate realistic-ish inference latency
    time.sleep(random.uniform(0.2, 1.2))

    prompt_tokens = sum(len(m.get("content", "").split()) for m in body.get("messages", [])) or random.randint(20, 200)
    prompt_tokens = int(prompt_tokens * 1.3)  # rough word->token fudge factor
    reply = random.choice(FAKE_REPLIES)
    completion_tokens = int(len(reply.split()) * 1.3)

    # occasionally simulate a failure so the dashboard has an error rate to show
    if random.random() < 0.05:
        return JSONResponse(status_code=500, content={"error": {"message": "simulated upstream failure"}})

    return {
        "id": f"chatcmpl-{uuid.uuid4().hex[:12]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": body.get("model", "demo-model"),
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": reply},
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
        },
    }
