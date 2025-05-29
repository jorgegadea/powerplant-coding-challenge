from app.models import ProductionPlanRequest, ProductionPlanResponse
import logging


def calculate_production_plan(request: ProductionPlanRequest):
    """
    Calculates the optimal production plan for a given load and the available powerplants.

    Args:
        request (ProductionPlanRequest):  Input data including load, fuel prices, and powerplant specs.

    Returns:
        List[ProductionPlanResponse]: List with the production assigned to each powerplant.

    Raises:
        Exception: If an error occurs during the calculation for any plant.
    """
    load = request.load
    fuels = request.fuels
    plants = []

    # Calculate the total cost, pmax and pmin of each power plant
    for plant in request.power_plants:
        try:
            if plant.type == "gasfired":
                cost = fuels.gas_euro_per_MWh / plant.efficiency
                pmax = plant.pmax
                pmin = plant.pmin
            elif plant.type == "turbojet":
                cost = fuels.kerosine_euro_per_MWh / plant.efficiency
                pmax = plant.pmax
                pmin = plant.pmin
            elif plant.type == "windturbine":
                cost = 0.0
                # Adjust wind production
                pmax = plant.pmax * (fuels.wind_percentage / 100)
                pmin = plant.pmin * (fuels.wind_percentage / 100)
            else:
                continue # Skip unsupported plant types

            # Store plant info and calculated cost
            plants.append({
                "name": plant.name,
                "type": plant.type,
                "cost": cost,
                "pmin": pmin,
                "pmax": pmax,
                "efficiency": plant.efficiency
            })
        except Exception as e:
            logging.error(f"Error processing plant {plant.name}: {e}")
            raise

    # Sort plants by cost 
    plants.sort(key=lambda x: x['cost'])

    # Initialize remaining load and result list
    remaining_load = load
    result = []

    # Calculate the production plan
    for plant in plants:
        try:
            if remaining_load <=0:
                power = 0.0
            else:
                # We take the maximum between the minimum of the plant and the remaining load
                # and the minimum between the maximum of the plant and the result of the previous load
                # This ensures that we do not exceed the remaining load and respect the minimum of the plant
                power = min(plant["pmax"], max(plant["pmin"], remaining_load))
                power = round(power, 1)
                if power > remaining_load:
                    power = round(remaining_load, 1)
            result.append(ProductionPlanResponse(name=plant["name"], p=power))
            remaining_load -= power
        except Exception as e:
            logging.error(f"Error calculating power for plant {plant['name']}: {e}")
            raise

    # If there is negaative load, we adjust the last plant's production last power minus de remaining load
    # This is a workaround for the case where the last plant has a minimum production
    if remaining_load < 0 and result:
        result[-1].p = round(result[-1].p + remaining_load, 1)

    return result