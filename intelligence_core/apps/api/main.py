from fastapi import FastAPI
from pydantic import BaseModel
from intelligence_core.core.engine import UnifiedIntelligenceEngine


class DecisionRequest(BaseModel):
    payload: dict


app = FastAPI(title="META-GENIUSZ Intelligence Core API")
engine = UnifiedIntelligenceEngine(config={"policy": {"confidence_threshold": 0.5}})


@app.get("/v1/health")
async def health():
    return {"status": "ok"}


@app.post("/v1/decision")
async def decision(req: DecisionRequest):
    result = await engine.process(req.payload)
    return result
