import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_fuel_required(distance_km: float, mileage_kmpl: float):
    logging.debug(f'Calculating fuel required for distance: {distance_km} km and mileage: {mileage_kmpl} km/l')
    fuel_needed = distance_km / mileage_kmpl
    logging.debug(f'Fuel required: {fuel_needed} liters')
    return fuel_needed


def calculate_fuel_cost(fuel_needed: float, fuel_price: float):
    logging.debug(f'Calculating fuel cost for fuel needed: {fuel_needed} liters at price: {fuel_price} per liter')
    cost = fuel_needed * fuel_price
    logging.debug(f'Total fuel cost: {cost}')
    return cost