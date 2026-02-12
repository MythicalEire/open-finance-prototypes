from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Dict, Any
from errors import APIException, ErrorCode

router = APIRouter()

class AgentAuthRequest(BaseModel):
    """Request model for authorizing an AI agent for spending."""
    agent_id: str = Field(..., min_length=1, description="Unique identifier for the AI agent requesting authorization")
    spending_limit: float = Field(..., gt=0, description="Maximum transaction amount in the specified currency. Must not exceed $500 for automated approval.")
    currency: str = Field(default="USD", description="ISO 4217 currency code")
    merchant_category: str = Field(..., min_length=1, description="Target merchant category (e.g., 'restaurants', 'groceries'). Cannot be a prohibited category like gambling or crypto.")
    
    class Config:
        json_schema_extra = {
            "example": {
                "agent_id": "agent_ai_2026_001",
                "spending_limit": 250.00,
                "currency": "USD",
                "merchant_category": "restaurants"
            }
        }

@router.post(
    "/authorize-agent",
    summary="Authorize AI Agent for Spending",
    description="Authorizes an AI agent to perform transactions within defined guardrails. Validates spending limits and merchant category restrictions per governance policies.",
    response_description="Authorization consent token and constraints for the requested transaction"
)
async def authorize_agent(request: AgentAuthRequest) -> Dict[str, Any]:
    """Authorize an AI agent for spending with security guardrails.
    
    This endpoint implements the governance framework for agentic transactions:
    - Enforces spending limit caps (max $500 for automated approval)
    - Validates against prohibited merchant categories (gambling, casino, betting, crypto)
    - Returns a consent token for downstream transaction processing
    
    Args:
        request (AgentAuthRequest): Agent authorization request containing ID, spending limit, currency, and merchant category
    
    Returns:
        Dict: Authorization response with consent token and constraints
        
    Raises:
        HTTPException 403: If spending limit exceeds $500 or merchant category is prohibited
    """
    # 1. Check for Spending Limit Guardrail
    if request.spending_limit > 500:
        raise APIException(
            code=ErrorCode.LIMIT_EXCEEDED,
            message="Limit Exceeded: Transactions over $500 require human MFA step-up.",
            status_code=403,
            details={"max_allowed": 500, "requested": request.spending_limit}
        )

    # 2. Check for High-Risk Category Guardrail
    prohibited_categories = ["gambling", "casino", "betting", "crypto"]
    if request.merchant_category.lower() in prohibited_categories:
        raise APIException(
            code=ErrorCode.GOVERNANCE_VIOLATION,
            message=f"Governance Violation: AI Agents are prohibited from {request.merchant_category}.",
            status_code=403,
            details={"prohibited_category": request.merchant_category}
        )

    # 3. Success Path
    return {
        "status": "Authorized",
        "consent_id": "consent_tkn_2026_x99",
        "merchant_constraints": request.merchant_category,
        "message": "AI Agent authorized within defined guardrails."
    }