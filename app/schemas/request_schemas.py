# app/schemas/request_schema.py

from pydantic import BaseModel


class TripRequest(BaseModel):
    query: str