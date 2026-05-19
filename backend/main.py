from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Hectron Core", version="2026.1")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class ChatRequest(BaseModel):
    message: str
    model: str = "grok"

@app.get("/health")
def health():
    return {"status": "healthy", "version": "2026.1"}

@app.post("/chat")
async def chat(request: ChatRequest):
    # TODO: Integrar tu lógica completa de agentes aquí
    return {"response": f"Hectron: {request.message}", "model": request.model}

@app.websocket("/ws/agent")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"[Hectron Swarm] Procesando: {data}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)