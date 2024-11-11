import serial
import logging
import signal
import time
import requests

from config import settings
from models import SensorReading


# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Global flag to control the main loop
running = True


def signal_handler(sig, frame):
    global running
    running = False
    logging.info("Interrupt received. Stopping...")


def read_sensor(ser: serial.Serial) -> SensorReading:
    """Reads the sensor data from the serial port.

    Args:
        ser (serial.Serial): The serial object connected to the sensor.

    Returns:
        SensorReading or None: The sensor reading object or None if the reading failed.
    """
    try:
        logging.debug("Requesting sensor reading...")
        sensor_request_command = b"s"
        ser.write(sensor_request_command)
        response = ser.read_until().decode("utf-8").strip()

        # Validate and convert the response
        if response:
            value = float(response)
            reading = SensorReading.new_reading(value=value)
            logging.debug("Sensor response: %s", response)
            return reading
        else:
            logging.error("Empty response received from sensor")

    except ValueError:
        logging.error("Invalid sensor data received: %s", response)

    except Exception as e:
        logging.error("Error reading sensor: %s", str(e))

    # Return None in case of error or invalid data
    return None


def send_to_backend(sensor_reading: SensorReading):
    """
    Sends the sensor reading data to the backend.

    This function posts the sensor reading data to a specified backend URL
    in JSON format. It logs a success message if the operation succeeds,
    and logs appropriate error messages if any exceptions occur during the
    process.

    Parameters
    ----------
    sensor_reading : SensorReading
        The sensor reading object that contains the measurement data to
        be sent to the backend. This object should have a `model_dump_json`
        method that provides a JSON representation of the sensor reading.

    Raises
    ------
    requests.HTTPError
        If an HTTP error occurs during the POST request.
    Exception
        If any other error occurs during the process.

    Examples
    --------
    >>> sensor_reading = SensorReading.new_reading(value=23.5)
    >>> send_to_backend(sensor_reading)

    Notes
    -----
    - This function uses the `requests` library to send HTTP POST requests.
    - Ensure that `settings.backend_sensor_url` is properly configured with
      the backend endpoint URL.
    - This function relies on the `model_dump_json` method of the
      `SensorReading` object to serialize the data to JSON format.
    """

    try:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        response = requests.post(
            settings.backend_sensor_url,
            headers=headers,
            data=sensor_reading.model_dump_json(),
        )

        # Raise an exception for HTTP error responses
        response.raise_for_status()

        logging.debug("Successfully sent sensor reading to backend.")

    except requests.HTTPError as http_err:
        logging.error("HTTP error occurred: %s", str(http_err))
    except Exception as e:
        logging.error("Error sending to backend: %s", str(e))


def main():
    # Register the SIGINT handler to gracefully handle interrupt signals
    signal.signal(signal.SIGINT, signal_handler)
    try:
        # Configure the serial port with settings from the configuration
        with serial.Serial(
            port=settings.serial_port,
            baudrate=settings.serial_baud_rate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=settings.read_interval_s,
        ) as ser:

            logging.info("Starting periodic sensor reading...")

            # Main loop to read sensor data and send it to the backend
            while running:
                sensor_reading = read_sensor(ser)
                if sensor_reading:
                    send_to_backend(sensor_reading)
                time.sleep(settings.read_interval_s)  # Delay for the specified interval
    except Exception as e:
        # Log any exceptions that occur during the main loop
        logging.error("An error occurred: %s", str(e))
    finally:
        # Ensure the serial port is closed when the program exits
        logging.info("Serial port closed. Exiting...")


if __name__ == "__main__":
    main()
