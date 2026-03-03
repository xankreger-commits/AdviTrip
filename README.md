# 🚗 AdviTrip – Agentic Trip Planning System

AdviTrip is a production-style Agentic AI application that demonstrates structured planning, deterministic execution, and workflow state management.

It was built as a Level 4 Agent Architecture system to move beyond linear ReAct-style agents and implement a robust Planner–Executor design with named workflow state.

---

# 📌 Project Goal

To build a real-world Agentic AI system that:

- Uses an LLM as a structured planner
- Separates reasoning from execution
- Executes tools deterministically
- Manages intermediate outputs safely
- Supports branching workflows
- Avoids dependency corruption

This project is intentionally educational and architectural.

---

# 🧠 What Problem Does This Solve?

Traditional linear agents rely on:

```
previous_result
```

This fails when workflows branch.

Example:

Branch A:
- Fuel required → Fuel cost → Total cost → Split cost

Branch B:
- Distance → Travel time → Rest stops

In a linear system, one branch overwrites the other.

AdviTrip fixes this using named workflow state:

```
execution_state = {}
```

Each tool writes outputs under symbolic keys.

This ensures:

- No dependency collision
- Safe branching logic
- Deterministic execution
- Clear debugging

---

# 🏗 Architecture Overview

User  
→ Planner (LLM generates structured JSON plan)  
→ Executor (Deterministic execution engine)  
→ execution_state (Named state dictionary)  
→ Final Output  

---

# 🔥 Core Architectural Principles

1. Separate reasoning from execution  
2. Never rely on prompt for correctness  
3. Enforce validation in code  
4. Use named state for non-linear workflows  
5. Keep planner probabilistic, executor deterministic  

---

# 🛠 Available Tools

### 1️⃣ calculate_fuel_required
Inputs:
- distance_km
- mileage_kmpl  
Output:
- fuel_needed

---

### 2️⃣ calculate_fuel_cost
Inputs:
- fuel_needed
- fuel_price  
Output:
- fuel_cost

---

### 3️⃣ calculate_total_trip_cost
Inputs:
- fuel_cost
- toll_cost (optional)
- food_cost (optional)
- hotel_cost (optional)  
Output:
- total_cost

---

### 4️⃣ estimate_travel_time
Inputs:
- distance_km
- avg_speed_kmph (optional, default assumed)  
Output:
- travel_time

---

### 5️⃣ plan_rest_stops
Inputs:
- total_travel_time
- rest_interval_hours (optional, default assumed)  
Output:
- rest_stops

---

### 6️⃣ split_trip_cost
Inputs:
- total_cost
- number_of_people  
Output:
- cost_per_person

---

# 🧩 Planner–Executor Contract

Planner outputs structured JSON like:

```json
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
    }
  ]
}
```

Executor resolves symbolic references:

- "fuel_needed"
- "fuel_cost"
- "total_cost"
- "travel_time"
- "rest_stops"

No `previous_result` allowed.

---

# 📂 Project Structure

```
AdviTrip/
│
├── app/
│   ├── main.py
│   ├── agent/
│   │   ├── planner.py
│   │   ├── executor.py
│   ├── tools/
│   │   ├── fuel_tools.py
│   │   ├── cost_tools.py
│   │   ├── time_tools.py
│   │   ├── split_tools.py
│   ├── schemas/
│   │   ├── request_schema.py
│   │   ├── plan_schema.py
│
├── requirements.txt
├── README.md
```

---

# 🚀 How To Run

1. Create virtual environment

```
python -m venv venv
```

2. Activate

Windows:
```
venv\Scripts\activate
```

Mac/Linux:
```
source venv/bin/activate
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Start server

```
uvicorn app.main:app --reload
```

5. Open:
```
http://127.0.0.1:8000/docs
```

---

# 🧪 Example Request

POST `/plan-trip`

```json
{
  "query": "Plan a 400 km trip. Mileage 18 km per litre. Fuel 105 rupees per litre. Toll 800. Food 1200. 4 people travelling."
}
```

---

# 📊 Example Execution State Output

```
{
  "fuel_needed": 22.22,
  "fuel_cost": 2333.33,
  "total_cost": 4333.33,
  "travel_time": 6.66,
  "rest_stops": 2,
  "cost_per_person": 1083.33
}
```

---

# 🧠 Key Lessons Learned

- Linear chaining fails for branching workflows
- Named state enables safe dependency resolution
- Prompt changes must align with architectural contract
- Strong models do not replace strong architecture
- Deterministic execution is mandatory in production

---

# 📈 Future Improvements

- Dependency validation layer
- Automatic re-planning on failure
- DAG-based execution (LangGraph style)
- Observability & tracing
- Model-agnostic abstraction
- LangChain-based rebuild

---

# 🏁 Learning Outcome

This project demonstrates transition from:

Toy Agent → Structured Workflow Engine

It is a foundational step before:

- LangChain Agents
- LangGraph DAG execution
- Enterprise-grade AI orchestration

---

# 📄 License

MIT License

---

# 🙌 Author

Built as part of a structured journey into Agentic AI system architecture and workflow engineering.