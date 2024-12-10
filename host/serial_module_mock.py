import math
import time
import logging


class SerialModuleMock:
    def __init__(self, port, baudrate, timeout, sensor_count):
        self.sensor_count = sensor_count

    def open(self):
        logging.info("Mock serial port opened")

    def close(self):
        logging.info("Mock serial port closed")

    def read_sensor_voltages(self):
        # Return the sine of the current time as a mock sensor reading
        mock_reading = [
            math.sin(1 / (i + 1) * time.time()) for i in range(self.sensor_count)
        ]
        logging.debug(f"Mock sensor response: {mock_reading}")
        return mock_reading
