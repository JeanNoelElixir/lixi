from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")


@app.get("/")
def root():
    return {"status": "LIXIA proxy OK"}


@app.post("/v1/messages")
async def proxy_messages(request: Request):
    """
    Proxy transparent vers l'API Anthropic.
    Respecte le mode demandé par le client : renvoie du JSON si stream=false,
    et du SSE (text/event-stream) si stream=true.
    """
    body = await request.body()

    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(
            "https://api.anthropic.com/v1/messages",
            content=body,
            headers={
                "Content-Type": "application/json",
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
            },
        )

    # On préserve le Content-Type retourné par Anthropic
    # (application/json pour stream=false, text/event-stream pour stream=true)
    media_type = resp.headers.get("content-type", "application/json")

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        media_type=media_type,
    )
