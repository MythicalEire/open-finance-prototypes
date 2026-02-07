from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import uuid

app = FastAPI(title="Mastercard Agentic Pay Prototype")

# This is the "Data Model" - what the API expects to receive
class AgentAuthRequest(BaseModel):
    agent_id: str
    spending_limit: float
    currency: str = "USD"
    merchant_category: str

@app.get("/")
def root():
    return {"message": "Welcome to the Agentic Pay Authorization API Prototype"}

@app.post("/authorize-agent")
async def authorize_agent(request: AgentAuthRequest):
    # PM LOGIC: Security Guardrail
    # If the limit is too high, we simulate a "Step-up Authentication" failure
    if request.spending_limit > 500:
        raise HTTPException(
            status_code=403, 
            detail="Limit Exceeded: Transactions over $500 require human MFA."
        )
    
    # Simulate generating a secure Mastercard Token
    token = f"MA-CONSENT-{uuid.uuid4().hex[:12].upper()}"
    
    return {
        "status": "Authorized",
        "consent_token": token,
        "expires_at": datetime.now() + timedelta(hours=1),
        "constraints": {
            "max_amount": request.spending_limit,
            "currency": request.currency,
            "allowed_merchant_cat": request.merchant_category
        }
    }
