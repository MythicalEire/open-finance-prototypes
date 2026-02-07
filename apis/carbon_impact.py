from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Dict, Any

router = APIRouter()

# Simple database of carbon factors (kg of CO2 per $1 spent)
# In a real MC product, this would come from a partner like Doconomy
CARBON_FACTORS: Dict[str, Dict[str, Any]] = {
    "4511": {"name": "Airlines", "factor": 0.85},
    "5411": {"name": "Grocery Stores", "factor": 0.12},
    "5541": {"name": "Gas Stations", "factor": 2.10},
    "5812": {"name": "Restaurants", "factor": 0.25}
}

class Transaction(BaseModel):
    """Transaction data for carbon impact enrichment."""
    mcc: str = Field(..., pattern="^\d{4}$", description="Merchant Category Code (MCC) - 4-digit code identifying merchant type")
    amount: float = Field(..., gt=0, description="Transaction amount in the specified currency. Used to calculate carbon footprint.")
    description: str = Field(..., min_length=1, description="Human-readable transaction description (e.g., 'Flight to New York' or 'Weekly groceries'")
    
    class Config:
        json_schema_extra = {
            "example": {
                "mcc": "4511",
                "amount": 250.00,
                "description": "Flight to New York"
            }
        }

@router.post(
    "/enrich-transaction",
    summary="Enrich Transaction with Carbon Impact Data",
    description="Calculates and returns carbon footprint data for a transaction based on merchant category. Supports ESG tracking and sustainability reporting.",
    response_description="Transaction enriched with carbon impact metrics and environmental insights"
)
async def enrich_transaction(tx: Transaction) -> Dict[str, Any]:
    """Enrich a transaction with carbon footprint and ESG impact data.
    
    This endpoint provides environmental impact analysis for transactions by:
    - Looking up carbon factors based on merchant category code (MCC)
    - Calculating total CO2 emissions for the transaction amount
    - Providing actionable insights for carbon footprint tracking
    
    Supported MCCs:
    - 4511: Airlines (0.85 kg CO2 per $1)
    - 5411: Grocery Stores (0.12 kg CO2 per $1)
    - 5541: Gas Stations (2.10 kg CO2 per $1)
    - 5812: Restaurants (0.25 kg CO2 per $1)
    - Other MCCs: 0.15 kg CO2 per $1 (default)
    
    Args:
        tx (Transaction): Transaction data including MCC, amount, and description
    
    Returns:
        Dict: Enriched transaction data with carbon footprint metrics and insights
    """
    # Lookup the factor based on the Merchant Category Code (MCC)
    category_data = CARBON_FACTORS.get(tx.mcc, {"name": "General Retail", "factor": 0.15})
    
    # Calculate impact
    carbon_kg = round(tx.amount * category_data["factor"], 2)
    
    return {
        "original_transaction": tx.description,
        "merchant_category": category_data["name"],
        "carbon_footprint_kg": carbon_kg,
        "insights": f"This purchase contributed {carbon_kg}kg of CO2 to your monthly limit."
    }