import random
import time
from threading import RLock
from src.utils import data_lock, temperature_queue, latest_temperatures

# Simulate temperature sensor readings
def simulate_sensor(sensor_id):
    while True:
        temperature = random.randint(15, 40)  # Generate a random temperature
        with data_lock:
            latest_temperatures[sensor_id] = temperature  # Update the latest temperature

        if not temperature_queue.full():
            temperature_queue.put(temperature)  # Add the temperature to the queue
        else:
            temperature_queue.get()  # Remove old readings if the queue is full
            temperature_queue.put(temperature)  # Add the new one

        time.sleep(1)  # Wait before simulating next reading
