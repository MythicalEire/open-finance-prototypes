from fastapi import FastAPI
from apis.agent_pay import router as agent_router
from apis.carbon_impact import router as carbon_router

openapi_tags = [
    {
        "name": "Agentic Pay",
        "description": "Authorize AI agents with spend guardrails and policy enforcement. Value: reduces risk, enforces governance, and enables safe autonomous payments.",
        "externalDocs": {
            "description": "Product Vision",
            "url": "https://github.com/MythicalEire/open-finance-prototypes#product-vision"
        }
    },
    {
        "name": "ESG Enrichment",
        "description": "Enrich transactions with carbon-impact metrics to surface sustainability insights and enable reporting.",
        "externalDocs": {
            "description": "Carbon methodology",
            "url": "https://github.com/MythicalEire/open-finance-prototypes#future-enhancements"
        }
    }
]

app = FastAPI(
    title="Mastercard Open Finance Gateway",
    description="Prototype gateway demonstrating agent governance + ESG enrichment. Shows business value: safer automated payments and sustainability transparency.",
    version="1.0.0",
    contact={"name": "Maintainer", "email": "you@example.com"},
    openapi_tags=openapi_tags,
)

# This is the "Stitching" part
app.include_router(agent_router, prefix="/agent", tags=["Agentic Pay"])
app.include_router(carbon_router, prefix="/carbon", tags=["ESG Enrichment"])

@app.get("/")
def root():
    return {"message": "Gateway Online"}
