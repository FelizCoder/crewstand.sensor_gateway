# serial_module.py

import serial
import logging

class SerialModule:
    def __init__(self, port, baudrate, timeout, sensor_count):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

        if sensor_count == 1:
            self.request_command = b"0"
        else:
            self.request_command = b"s"

    def open(self):
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                # Default parity and stopbits settings align with common UART configuration
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
            self.ser.write(self.request_command)
            response = self.ser.read_until().decode("utf-8").strip().split(",")
            logging.debug(f"Sensor response: {response}")
            if response:
                try:
                    return [float(reading) for reading in response]
                except ValueError:
                    logging.error("Invalid floating-point value(s) in sensor response")
                    return None
            else:
                logging.error("Empty response received from sensor")
                return None
        except Exception as e:
            logging.error(f"Error reading sensor: {str(e)}")
            return None
