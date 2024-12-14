import numpy as np


class MCU:
    def __init__(self, id):
        self.id = id  # Unique identifier for the sensor
        self.description = "MCU"
        self.bitSize = None  # Unit of measurement (e.g., Celsius, Fahrenheit, etc.)
        self.operation_freq = None
        self.peripherals = {"SENSOR": [], "ACTUATOR": [], "MEMORY": [], "MCU": []}
        self.memory = {}
        self.pointers = []
        self.manufacturer = None
        self.model_name = None
        self.release_year = None

    def calibrate(self,  operation_frequency, bit_size):
        self.operation_freq = operation_frequency
        self.bitSize = bit_size

    def manufacturer_info(self, manufacturer, model_name, year):
        self.manufacturer = manufacturer
        self.model_name = model_name
        self.release_year = year

    def connect(self, obj):
        self.peripherals[obj.description].append(obj)

    def __str__(self):
        return f"MCU ID: {self.id}, Bit size: {self.bit_size}, Operation frequency: {self.operation_frequency},"\
                f"Peripherals: {self.peripherals}"
