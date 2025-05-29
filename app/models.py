from pydantic import BaseModel, Field
from typing import List

class Fuels(BaseModel):
    """
    Represents the fuel prices and wind percentage for the calculation.
    The field names are mapped from the input JSON using aliases.
    """
    gas_euro_per_MWh: float = Field(alias="gas(euro/MWh)")
    kerosine_euro_per_MWh: float = Field(alias="kerosine(euro/MWh)")
    co2_euro_per_MWh: float = Field(alias="co2(euro/ton)")
    wind_percentage: float = Field(alias="wind(%)")

class PowerPlant(BaseModel):
    """
    Represents a powerplant with its technical characteristics.
    """
    name: str
    type: str
    efficiency: float
    pmin: float
    pmax: float

class ProductionPlanRequest(BaseModel):
    """
    Input model for the production plan endpoint.
    Includes the load, fuel prices, and list of powerplants.
    """
    load: float
    fuels: Fuels
    power_plants: List[PowerPlant] = Field(alias="powerplants")

class ProductionPlanResponse(BaseModel):
    """
    Output model for the production plan.
    Includes the name of the powerplant and the assigned production.
    """
    name: str
    p: float