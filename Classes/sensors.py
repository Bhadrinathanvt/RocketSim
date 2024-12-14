import numpy as np


class SENSOR:
    def __init__(self, sensor_id, sensor_type, unit):
        self.id = sensor_id  # Unique identifier for the sensor
        self.sensor_type = sensor_type  # Type of the sensor (e.g., temperature, humidity, etc.)
        self.unit = unit  # Unit of measurement (e.g., Celsius, Fahrenheit, etc.)
        self.description = "SENSOR"
        self.operation_freq = None
        self.value = None  # The current reading from the sensor
        self.buffer_size = None
        self.buffer = None
        self.last_value_time = None
        self.sensor_bias = None
        self.manufacturer = None
        self.model_name = None

    def get_value(self, value, time):
        if time // (1 / self.operation_freq) < 1e-6:
            self.value = value
        for i in range(self.buffer_size, 0, -1):
            self.buffer[i] = self.buffer[i - 1]
        self.buffer[0] = value

    def calibrate(self, operation_freq, buffer_size=1, sensor_bias=0):
        self.operation_freq = operation_freq
        self.buffer_size = buffer_size
        self.buffer = np.zeros(self.buffer_size)
        self.sensor_bias = sensor_bias

    def read_sensor(self):
        return self.buffer[self.buffer_size - 1]

    def manufacture_info(self, manufacturer, model_name):
        self.manufacturer = manufacturer
        self.model_name = model_name

    def __str__(self):
        return f"Sensor ID: {self.sensor_id}, Type: {self.sensor_type}, Unit: {self.unit}, Buffer: {self.buffer}, " \
               f"Frequency: {self.operation_freq}, Buffer Size: {self.buffer_size}"
