import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

DEFAULT_SPEED_KMPH = 60  # Default highway assumption
DEFAULT_REST_INTERVAL_HOURS = 3  # Default rest every 3 hours


def estimate_travel_time(distance_km: float, avg_speed_kmph: float = None):
    """
    Estimate travel time in hours.
    If avg_speed_kmph is not provided, use default speed.
    """
    logging.debug(f"Estimating travel time for distance: {distance_km} km, avg_speed: {avg_speed_kmph} km/h")

    if distance_km is None:
        logging.error("Distance must be provided.")
        raise ValueError("Distance must be provided.")

    if avg_speed_kmph is None:
        avg_speed_kmph = DEFAULT_SPEED_KMPH
        logging.info(f"Using default speed: {avg_speed_kmph} km/h")

    if avg_speed_kmph <= 0:
        logging.error("Speed must be greater than zero.")
        raise ValueError("Speed must be greater than zero.")

    travel_time = distance_km / avg_speed_kmph
    logging.debug(f"Calculated travel time: {travel_time} hours")
    return travel_time


def plan_rest_stops(total_travel_time: float, rest_interval_hours: float = None):
    """
    Calculate number of rest stops.
    If rest_interval_hours is not provided, use default interval.
    """
    logging.debug(f"Planning rest stops for total travel time: {total_travel_time} hours, rest_interval: {rest_interval_hours} hours")

    if total_travel_time is None:
        logging.error("Total travel time must be provided.")
        raise ValueError("Total travel time must be provided.")

    if rest_interval_hours is None:
        rest_interval_hours = DEFAULT_REST_INTERVAL_HOURS
        logging.info(f"Using default rest interval: {rest_interval_hours} hours")

    if rest_interval_hours <= 0:
        logging.error("Rest interval must be greater than zero.")
        raise ValueError("Rest interval must be greater than zero.")

    rest_stops = int(total_travel_time // rest_interval_hours)
    logging.debug(f"Calculated number of rest stops: {rest_stops}")
    return rest_stops