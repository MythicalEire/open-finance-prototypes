from fastapi import FastAPI
from apis.agent_pay import router as agent_router
from apis.carbon_impact import router as carbon_router

app = FastAPI(
    title="Mastercard Open Finance Gateway",
    description="2026 Strategy Prototypes",
    version="1.0.0"
)

# This is the "Stitching" part
app.include_router(agent_router, prefix="/agent", tags=["Agentic Pay"])
app.include_router(carbon_router, prefix="/carbon", tags=["ESG Enrichment"])

@app.get("/")
def root():
    return {"message": "Gateway Online"}
