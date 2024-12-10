import serial
import logging


class SerialModule:
    def __init__(self, port, baudrate, timeout, sensor_count):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

        if sensor_count == 1:
            self.request_bytes = b"0"
        else:
            self.request_bytes = b"s"

    def open(self):
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=self.timeout,
            )
            logging.info(f"Serial port {self.port} opened successfully")
        except serial.SerialException as e:
            logging.error(f"Failed to open serial port {self.port}: {str(e)}")
            raise

    def close(self):
        if self.ser:
            self.ser.close()
            logging.info(f"Serial port {self.port} closed")

    def read_sensor_voltages(self):
        try:
            if not self.ser:
                raise ValueError("Serial port not opened")
            self.ser.write(self.request_bytes)
            response = self.ser.read_until().decode("utf-8").strip().split(",")
            logging.debug(f"Sensor response: {response}")
            if response:
                return [float(reading) for reading in response]
            else:
                logging.error("Empty response received from sensor")
        except ValueError as e:
            logging.error(f"Invalid sensor data received: {str(e)}")
        except Exception as e:
            logging.error(f"Error reading sensor: {str(e)}")
        return None
