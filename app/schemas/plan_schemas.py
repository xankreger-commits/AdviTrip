# app/schemas/plan_schema.py

from pydantic import BaseModel
from typing import List, Literal, Optional, Union


class PlanStep(BaseModel):
    tool: Literal[
        "calculate_fuel_required",
        "calculate_fuel_cost",
        "calculate_total_trip_cost",
        "estimate_travel_time",
        "plan_rest_stops",
        "split_trip_cost"
    ]

    # --- Fuel calculation ---
    distance_km: Optional[Union[float, str]] = None
    mileage_kmpl: Optional[Union[float, str]] = None

    fuel_needed: Optional[Union[float, str]] = None
    fuel_price: Optional[Union[float, str]] = None
    fuel_cost: Optional[Union[float, str]] = None

    # --- Cost breakdown ---
    toll_cost: Optional[float] = None
    food_cost: Optional[float] = None
    hotel_cost: Optional[float] = None

    # --- Time ---
    avg_speed_kmph: Optional[float] = None
    rest_interval_hours: Optional[float] = None
    total_travel_time: Optional[Union[float, str]] = None

    # --- Split ---
    total_cost: Optional[Union[float, str]] = None
    number_of_people: Optional[int] = None


class Plan(BaseModel):
    steps: List[PlanStep]