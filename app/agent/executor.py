# app/agent/executor.py

from app.schemas.plan_schemas import Plan
from app.tools import fuel_tools, cost_tools, time_tools, split_tools


def resolve(value, state):
    """
    Resolve value from execution state.
    """
    if isinstance(value, str):
        if value in state:
            return state[value]
        else:
            raise ValueError(f"State key '{value}' not found.")
    return value


def execute_plan(plan: Plan):

    execution_state = {}
    steps_results = []

    for step in plan.steps:

        # 1️⃣ Fuel Required
        if step.tool == "calculate_fuel_required":
            result = fuel_tools.calculate_fuel_required(
                step.distance_km,
                step.mileage_kmpl
            )
            execution_state["fuel_needed"] = result

        # 2️⃣ Fuel Cost
        elif step.tool == "calculate_fuel_cost":
            result = fuel_tools.calculate_fuel_cost(
                resolve(step.fuel_needed, execution_state),
                step.fuel_price
            )
            execution_state["fuel_cost"] = result

        # 3️⃣ Total Cost
        elif step.tool == "calculate_total_trip_cost":
            result = cost_tools.calculate_total_trip_cost(
                resolve(step.fuel_cost, execution_state),
                step.toll_cost,
                step.food_cost,
                step.hotel_cost
            )
            execution_state["total_cost"] = result

        # 4️⃣ Travel Time
        elif step.tool == "estimate_travel_time":
            result = time_tools.estimate_travel_time(
                step.distance_km,
                step.avg_speed_kmph
            )
            execution_state["travel_time"] = result

        # 5️⃣ Rest Stops
        elif step.tool == "plan_rest_stops":
            result = time_tools.plan_rest_stops(
                resolve(step.total_travel_time, execution_state),
                step.rest_interval_hours
            )
            execution_state["rest_stops"] = result

        # 6️⃣ Split Cost
        elif step.tool == "split_trip_cost":
            result = split_tools.split_trip_cost(
                resolve(step.total_cost, execution_state),
                step.number_of_people
            )
            execution_state["cost_per_person"] = result

        else:
            raise ValueError(f"Unknown tool: {step.tool}")

        steps_results.append(result)

    return {
        "steps_executed": steps_results,
        "execution_state": execution_state,
        "final_result": execution_state
    }