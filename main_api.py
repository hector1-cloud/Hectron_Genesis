from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.abada_agent import HectronAgent, omega_matrix

app = FastAPI(title="HECTRON-Ψ API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
agent = HectronAgent("Abada Node")

class Decree(BaseModel):
    input: str

@app.post("/decide")
async def decide(decree: Decree):
    result = agent.decide(decree.input)
    return {"result": result, "omega": omega_matrix()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
