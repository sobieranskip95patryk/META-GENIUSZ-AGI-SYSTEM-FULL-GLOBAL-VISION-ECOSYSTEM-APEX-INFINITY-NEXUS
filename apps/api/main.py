from fastapi import FastAPI, HTTPException

app = FastAPI(title="MetaGenius Core API")

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/v1/orchestrator/initiate")
async def initiate_orchestrator():
    # placeholder: will call OrchestratorBridge in infra
    return {"result": "initiated"}
