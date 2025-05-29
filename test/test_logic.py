import pytest
from app.logic import calculate_production_plan
from app.models import ProductionPlanRequest, Fuels, PowerPlant

def test_simple_case():
    """
    Simple case with wind and gas. Checks the correct wind allocation and total power.
    """
    request = ProductionPlanRequest(
        load=100,
        fuels=Fuels(
            gas_euro_per_MWh=10,
            kerosine_euro_per_MWh=20,
            co2_euro_per_MWh=0,
            wind_percentage=50
        ),
        power_plants=[
            PowerPlant(name="wind1", type="windturbine", efficiency=1, pmin=0, pmax=60),
            PowerPlant(name="gas1", type="gasfired", efficiency=0.5, pmin=0, pmax=100),
        ]
    )
    result = calculate_production_plan(request)
    # The total power should equal the load
    total_power = sum(p.p for p in result)
    assert abs(total_power - 100) < 0.1
    # The wind turbine should produce 30 (50% of 60)
    wind = next(p for p in result if p.name == "wind1")
    assert abs(wind.p - 30) < 0.1


def test_zero_load():
    """
    Test with zero load. All plants should produce zero.
    """
    request = ProductionPlanRequest(
        load=0,
        fuels=Fuels(
            gas_euro_per_MWh=10,
            kerosine_euro_per_MWh=20,
            co2_euro_per_MWh=0,
            wind_percentage=100
        ),
        power_plants=[
            PowerPlant(name="wind1", type="windturbine", efficiency=1, pmin=0, pmax=60),
            PowerPlant(name="gas1", type="gasfired", efficiency=0.5, pmin=0, pmax=100),
        ]
    )
    result = calculate_production_plan(request)
    # All plants should produce zero
    assert all(p.p == 0 for p in result)


def test_negative_load_adjustment():
    """
    Test adjustment when the last plant's pmin is greater than the remaining load.
    """
    request = ProductionPlanRequest(
        load=90,
        fuels=Fuels(
            gas_euro_per_MWh=10,
            kerosine_euro_per_MWh=20,
            co2_euro_per_MWh=0,
            wind_percentage=0
        ),
        power_plants=[
            PowerPlant(name="gas1", type="gasfired", efficiency=1, pmin=0, pmax=50),
            PowerPlant(name="gas2", type="gasfired", efficiency=1, pmin=40, pmax=100),
        ]
    )
    result = calculate_production_plan(request)
    # The total power should equal the load
    total_power = sum(p.p for p in result)
    assert abs(total_power - 90) < 0.1
    # The last plant should produce 40 (not 50)
    last = next(p for p in result if p.name == "gas2")
    assert abs(last.p - 40) < 0.1


def test_wind_zero_percent():
    """
    Test that windturbine produces zero when wind percentage is 0.
    """
    request = ProductionPlanRequest(
        load=50,
        fuels=Fuels(
            gas_euro_per_MWh=10,
            kerosine_euro_per_MWh=20,
            co2_euro_per_MWh=0,
            wind_percentage=0
        ),
        power_plants=[
            PowerPlant(name="wind1", type="windturbine", efficiency=1, pmin=0, pmax=60),
            PowerPlant(name="gas1", type="gasfired", efficiency=1, pmin=0, pmax=100),
        ]
    )
    result = calculate_production_plan(request)
    # The wind turbine should produce zero
    wind = next(p for p in result if p.name == "wind1")
    assert wind.p == 0
    # The gas plant should produce the full load
    total_power = sum(p.p for p in result)
    assert abs(total_power - 50) < 0.1


def test_pmin_greater_than_load():
    """
    Test when the only plant has pmin greater than the load. Should adjust to match load.
    """
    request = ProductionPlanRequest(
        load=30,
        fuels=Fuels(
            gas_euro_per_MWh=10,
            kerosine_euro_per_MWh=20,
            co2_euro_per_MWh=0,
            wind_percentage=0
        ),
        power_plants=[
            PowerPlant(name="gas1", type="gasfired", efficiency=1, pmin=50, pmax=100),
        ]
    )
    result = calculate_production_plan(request)
    # There is only one plant, its pmin is 50 but the load is 30, so it should adjust to 30
    assert len(result) == 1
    assert abs(result[0].p - 30) < 0.1