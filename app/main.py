# app/main.py

from fastapi import FastAPI
from app.schemas.request_schemas import TripRequest
from app.agent.planner import create_plan
from app.agent.executor import execute_plan

app = FastAPI(title="TripVisor - Smart Road Trip Agent")


@app.post("/plan-trip")
def plan_trip(request: TripRequest):
    print("Received trip request:", request.query)

    plan = create_plan(request.query)
    print("Generated plan:", plan)
    print("Moving to execution...")
    execution = execute_plan(plan)

    return {
        "plan": plan.dict(exclude_none=True),
        "execution": execution
    }