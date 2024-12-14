import numpy as np


class ACTUATOR:
    def __init__(self, id, actuator_type):
        self.id = id  # Unique identifier for the sensor
        self.actuator_type = actuator_type
        self.description = "ACTUATOR"
        # Type of the actuators: Fuel burn control, Thrust vector control, Fin control, Parachute discharge
        self.operation_freq = None
        self.value = None  # The current output from actuator
        self.buffer_size = None
        self.buffer = None
        self.last_value_time = None

    def calibrate(self, operation_freq, buffer_size=1):
        self.operation_freq = operation_freq
        self.buffer_size = buffer_size
        self.buffer = np.zeros(self.buffer_size)
