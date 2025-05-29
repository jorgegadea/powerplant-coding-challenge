from fastapi import FastAPI, HTTPException
from app.models import ProductionPlanRequest, ProductionPlanResponse
from app.logic import calculate_production_plan
from typing import List
import logging


app = FastAPI()

@app.post("/productionplan", response_model=List[ProductionPlanResponse])
def get_production_plan(request: ProductionPlanRequest):
    """
    Endpoint to calculate the production plan for a given load and available powerplants.

    
    Returns a list with the production assigned to each powerplant.
    Args:
        request (ProductionPlanRequest): Receives a POST request with the required load, fuel prices, and powerplant data.

    Raises:
        HTTPException: If an error occurs during the calculation, it raises a 500 Internal Server Error.

    Returns:
        List[ProductionPlanResponse] : Returns a list with the production assigned to each powerplant.
    """
    try:
        return calculate_production_plan(request)
    except Exception as e:
        logging.error(f"Error calculating production plan: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
