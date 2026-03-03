import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def split_trip_cost(total_cost: float, number_of_people: int):
    """
    Split total trip cost among number of people.

    Returns cost per person.
    """
    logging.debug(f"Received total_cost: {total_cost}, number_of_people: {number_of_people}")

    if total_cost is None:
        logging.error("Total cost must be provided.")
        raise ValueError("Total cost must be provided.")

    if number_of_people is None:
        logging.error("Number of people must be provided.")
        raise ValueError("Number of people must be provided.")

    if number_of_people <= 0:
        logging.error("Number of people must be greater than zero.")
        raise ValueError("Number of people must be greater than zero.")

    cost_per_person = round(total_cost / number_of_people, 2)
    logging.debug(f"Calculated cost per person: {cost_per_person}")

    return cost_per_person