from Classes.sensors import SENSOR
from Classes.mcu import MCU
sensor1 = SENSOR("IMU1", "Position", "meters")
sensor2 = SENSOR("IMU2", "Position", "meters")
sensor3 = SENSOR("Temp1", "Temperature", "Kelvin")
sensor4 = SENSOR("Pressure1", "Pressure", "Pascal")

sensor1.calibrate(1e3, 4, 0.4)
sensor2.calibrate(2e3, 8, 0.1)

mcu = MCU("Master")

Sensors = [sensor1, sensor2, sensor3, sensor4]
MCUs = [mcu]
Memory = []
Actuator = []
