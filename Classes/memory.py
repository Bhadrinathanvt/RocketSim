import numpy as np


class MEM:
    def __init__(self, id):
        self.id = id  # Unique identifier for the sensor
        self.description = "MEMORY"
        self.manufacturer = None  # Type of the sensor (e.g., temperature, humidity, etc.)
        self.address = None
        self.writeSize = None  # Unit of measurement (e.g., Celsius, Fahrenheit, etc.)
        self.capacity = None

    def calibrate(self):
        pass

    def connect(self, obj):
        self.peripherals[obj.description].append(obj)

    def __str__(self):
        return f"MCU ID: {self.sensor_id}, Type: {self.sensor_type}, Unit: {self.unit}, Buffer: {self.buffer}, " \
               f"Frequency: {self.operation_freq}, Buffer Size: {self.buffer_size}"

