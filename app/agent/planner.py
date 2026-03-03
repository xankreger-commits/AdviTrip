# # app/agent/planner.py

# import json
# import cohere
# from app.config import COHERE_API_KEY, COHERE_MODEL
# from app.schemas.plan_schemas import Plan

# co = cohere.Client(COHERE_API_KEY)

# PLANNER_PROMPT = """
# You are a trip planning agent.

# Break the user's trip request into executable steps.

# Available tools:
# - calculate_fuel_required
# - calculate_fuel_cost
# - calculate_total_trip_cost
# - estimate_travel_time
# - plan_rest_stops
# - split_trip_cost

# Rules:
# - Use "previous_result" to reference output of previous step.
# - calculate_fuel_cost must use fuel_needed and fuel_price.
# - calculate_total_trip_cost must use fuel_cost.
# - plan_rest_stops must use total_travel_time.
# - split_trip_cost must use total_cost.
# - Do NOT compute results yourself.
# - Return STRICT JSON only.

# Example:

# {
#   "steps": [
#     {
#       "tool": "calculate_fuel_required",
#       "distance_km": 300,
#       "mileage_kmpl": 18
#     },
#     {
#       "tool": "calculate_fuel_cost",
#       "fuel_needed": "previous_result",
#       "fuel_price": 105
#     },
#     {
#       "tool": "calculate_total_trip_cost",
#       "fuel_cost": "previous_result",
#       "toll_cost": 800,
#       "food_cost": 1200
#     }
#   ]
# }
# """


# def create_plan(user_query: str) -> Plan:

#     response = co.chat(
#         model=COHERE_MODEL,
#         message=f"{PLANNER_PROMPT}\nUser query: {user_query}",
#         temperature=0
#     )

#     text = response.text.strip()

#     # Extract JSON safely
#     start = text.find("{")
#     end = text.rfind("}") + 1

#     if start == -1 or end == -1:
#         raise ValueError("Invalid JSON from planner")

#     json_str = text[start:end]
#     plan_dict = json.loads(json_str)

#     return Plan(**plan_dict)



# app/agent/planner.py




import json
from groq import Groq
from app.config import GROQ_API_KEY
from app.schemas.plan_schemas import Plan

# Initialize Groq client
client = Groq(
    api_key=GROQ_API_KEY,
)

PLANNER_PROMPT = """
You are a structured trip planning agent.

Your job is to break the user's request into ordered executable steps.

You MUST return STRICT JSON only.
The JSON must be directly parsable using json.loads() in Python.
Do NOT include explanations.
Do NOT include markdown.
Do NOT compute results.

--------------------------------------
AVAILABLE TOOLS
--------------------------------------

1. calculate_fuel_required
   Inputs:
   - distance_km (number)
   - mileage_kmpl (number)
   Output stored as: "fuel_needed"

2. calculate_fuel_cost
   Inputs:
   - fuel_needed (number OR reference to state key)
   - fuel_price (number)
   Output stored as: "fuel_cost"

3. calculate_total_trip_cost
   Inputs:
   - fuel_cost (number OR reference to state key)
   - toll_cost (number, optional default 0)
   - food_cost (number, optional default 0)
   - hotel_cost (number, optional default 0)
   Output stored as: "total_cost"

4. estimate_travel_time
   Inputs:
   - distance_km (number)
   - avg_speed_kmph (number, optional — default assumed if missing)
   Output stored as: "travel_time"

5. plan_rest_stops
   Inputs:
   - total_travel_time (number OR reference to state key)
   - rest_interval_hours (number, optional — default assumed if missing)
   Output stored as: "rest_stops"

6. split_trip_cost
   Inputs:
   - total_cost (number OR reference to state key)
   - number_of_people (number)
   Output stored as: "cost_per_person"

--------------------------------------
CRITICAL RULES
--------------------------------------

1. NEVER use "previous_result".
2. ALWAYS reference outputs using explicit state keys:
   - "fuel_needed"
   - "fuel_cost"
   - "total_cost"
   - "travel_time"
   - "rest_stops"
3. Only use tools that are relevant to the user request.
4. If a value is not mentioned in the user query and is optional, omit it.
5. Do NOT invent random numbers.
6. Each step must include only fields relevant to that tool.
7. Output must follow this exact structure:

{
  "steps": [
    {
      "tool": "tool_name",
      "field1": value,
      "field2": value
    }
  ]
}

--------------------------------------
EXAMPLE
--------------------------------------

User Query:
"Plan a 400 km trip. Mileage 18 km per litre. Fuel 105 rupees per litre. 4 people travelling."

Correct Output:

{
  "steps": [
    {
      "tool": "calculate_fuel_required",
      "distance_km": 400,
      "mileage_kmpl": 18
    },
    {
      "tool": "calculate_fuel_cost",
      "fuel_needed": "fuel_needed",
      "fuel_price": 105
    },
    {
      "tool": "calculate_total_trip_cost",
      "fuel_cost": "fuel_cost"
    },
    {
      "tool": "split_trip_cost",
      "total_cost": "total_cost",
      "number_of_people": 4
    }
  ]
}

--------------------------------------
Now generate the plan for the user query.
"""







def create_plan(user_query: str) -> Plan:
    # Use Groq client to generate chat completion
    print("Generating plan with Groq...")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{PLANNER_PROMPT}\nUser query: {user_query}",
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    # Extract the response text
    text = chat_completion.choices[0].message.content.strip()
    print("Received response from Groq:")
    print(text)

    # Extract JSON safely
    start = text.find("{")
    end = text.rfind("}") + 1

    if start == -1 or end == -1:
        raise ValueError("Invalid JSON from planner")
    
    print(f"Extracted JSON substring: {text[start:end]}")

    json_str = text[start:end]
    print(f"JSON string to parse: {json_str}")
    plan_dict = json.loads(json_str)
    print(f"Parsed plan dictionary: {plan_dict}")
    return Plan(**plan_dict)