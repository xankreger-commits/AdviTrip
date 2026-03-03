import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def calculate_total_trip_cost(
    fuel_cost: float,
    toll_cost: float = 0,
    food_cost: float = 0,
    hotel_cost: float = 0
):
    """
    Calculate total trip cost.
    """

    logging.debug("Starting calculation of total trip cost.")
    
    if fuel_cost is None:
        logging.error("Fuel cost must be provided.")
        raise ValueError("Fuel cost must be provided.")
    
    logging.debug(f"Fuel cost: {fuel_cost}")
    logging.debug(f"Toll cost: {toll_cost}")
    logging.debug(f"Food cost: {food_cost}")
    logging.debug(f"Hotel cost: {hotel_cost}")

    toll_cost = toll_cost or 0
    food_cost = food_cost or 0
    hotel_cost = hotel_cost or 0

    total_cost = fuel_cost + toll_cost + food_cost + hotel_cost
    logging.debug(f"Total trip cost calculated: {total_cost}")

    return total_cost