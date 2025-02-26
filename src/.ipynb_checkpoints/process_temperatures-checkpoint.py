import time
from src.utils import temperature_averages, temperature_queue, data_lock, condition

# Process temperatures and calculate the average for each sensor
def process_temperatures():
    while True:
        with data_lock:
            while temperature_queue.empty():  # Wait if no temperatures are in the queue
                condition.wait()

            readings = list(temperature_queue.queue)  # Get readings from the queue
            sensor_data = {}

            # Group the readings by sensor and calculate their averages
            for temperature in readings:
                sensor_id = f"sensor_{readings.index(temperature) + 1}"  # Get the sensor ID
                if sensor_id not in sensor_data:
                    sensor_data[sensor_id] = []
                sensor_data[sensor_id].append(temperature)

            # Calculate and update the average for each sensor
            for sensor_id, sensor_readings in sensor_data.items():
                avg_temperature = sum(sensor_readings) / len(sensor_readings)
                temperature_averages[sensor_id] = avg_temperature  # Store the average for each sensor

        time.sleep(1)  # Wait before recalculating the average
