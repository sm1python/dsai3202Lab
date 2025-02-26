from threading import RLock, Condition
import queue
# Shared Data Structures
latest_temperatures = {}  # Stores the latest temperatures for each sensor
temperature_averages = {}  # Stores the average temperature
temperature_queue = queue.Queue(maxsize=10)  # Queue to hold temperature readings

# Lock to synchronize access to shared data
data_lock = RLock()

condition = Condition()  # Condition