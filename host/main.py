import serial
import logging
import signal
import time
import requests

from config import settings
from models import SensorReading, ValueRange


# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Global flag to control the main loop
running = True


def signal_handler(sig, frame):
    global running
    running = False
    logging.info("Interrupt received. Stopping...")


def interpolate_measurement(
    voltage: float, voltage_range: ValueRange, measurement_range: ValueRange
) -> float:
    """
    Linearly interpolate a measurement value based on the given voltage and specified ranges.

    This function performs a linear interpolation to convert a voltage reading
    into a measurement value (e.g., flow rate) based on provided voltage
    and measurement ranges.

    Parameters
    ----------
    voltage : float
        The voltage value from the sensor.
    voltage_range : tuple[float, float]
        The minimum and maximum voltage values that the sensor can output.
    measurement_range : tuple[float, float]
        The minimum and maximum measurement values that correspond to the
        voltage range.

    Returns
    -------
    float
        The interpolated measurement value.

    Notes
    -----
    The interpolation formula used is:

    .. math::
        measurement = (voltage - voltage_{min}) \times \frac{(measurement_{max} - measurement_{min})}{(voltage_{max} - voltage_{min})} + measurement_{min}

    where `voltage_{min}` and `voltage_{max}` are the minimum and maximum
    values of the voltage range, and `measurement_{min}` and `measurement_{max}`
    are the minimum and maximum values of the measurement range.

    Examples
    --------
    >>> voltage = 2.5
    >>> voltage_range = (0.0, 5.0)
    >>> measurement_range = (0.0, 100.0)
    >>> interpolate_measurement(voltage, voltage_range, measurement_range)
    50.0
    """

    slope = (measurement_range[1] - measurement_range[0]) / (
        voltage_range[1] - voltage_range[0]
    )
    offset = measurement_range[0]
    measurement = (voltage - voltage_range[0]) * slope + offset

    return measurement


def read_sensor_voltages(ser: serial.Serial) -> list[float]:
    """
    Reads the sensor data from the serial port.

    Args:
        ser (serial.Serial): The serial object connected to the sensor.
        sensor_id (int): The ID of the sensor to read.

    Returns:
        SensorReading or None: The sensor reading object or None if the reading failed.

    Raises:
        ValueError: If the sensor data received is not a valid float.
        Exception: If any other error occurs during the reading process.

    Notes:
        This function sends a command to the sensor to request a reading and then waits for a response.
        If the response is empty or cannot be converted to a float, an error is logged and None is returned.
    """

    try:
        if settings.sensor_count == 1:
            sensor_bytes = b"0"
        else:
            sensor_bytes = b"s"
        logging.debug("Requesting sensor reading...")
        ser.write(sensor_bytes)
        response = ser.read_until().decode("utf-8").strip().split(",")
        logging.debug("Sensor response: %s", response)

        # Validate and convert the response
        if response:
            voltage = [float(reading) for reading in response]
            return voltage
        else:
            logging.error("Empty response received from sensor")

    except ValueError:
        logging.error("Invalid sensor data received: %s", response)

    except Exception as e:
        logging.error("Error reading sensor: %s", str(e))

    # Return None in case of error or invalid data
    return None


def send_to_backend(sensor_reading: SensorReading, sensor_id: int) -> None:
    """
    Send a sensor reading to the backend server.

    Parameters
    ----------
    sensor_reading : SensorReading
        The sensor reading object to be sent.
    sensor_id : int
        The id of the sensor that generated the reading.

    Returns
    -------
    None

    Raises
    ------
    HTTPError
        If the HTTP response from the backend server indicates an error.
    Exception
        If any other error occurs during the request.

    Notes
    -----
    This function sends a POST request to the backend server with the sensor reading data.
    The request includes headers specifying the content type and the data in JSON format.
    If the request is successful, a debug message is logged.
    If an HTTP error occurs, an error message is logged.
    If any other exception occurs, an error message is logged.

    Examples
    --------
    >>> sensor_reading = SensorReading(value=42.0, timestamp=time.time_ns())
    >>> send_to_backend(sensor_reading, sensor_id=123)
    Successfully sent sensor reading to backend.
    """

    try:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        sensor_url_path = (
            f"{settings.backend_sensor_url}v1/sensors/flowmeters/{sensor_id}/reading"
        )

        response = requests.post(
            sensor_url_path,
            headers=headers,
            data=sensor_reading.model_dump_json(),
            timeout=settings.read_interval_s,
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
                start_time = time.time_ns()
                sensor_voltages = read_sensor_voltages(ser)
                if sensor_voltages:
                    for i in range(settings.sensor_count):
                        measurement = interpolate_measurement(
                            sensor_voltages[i],
                            settings.voltage_range,
                            settings.measurement_range[i],
                        )
                        measurement_reading = SensorReading(
                            value=measurement,
                            timestamp_ns=start_time,
                        )
                        send_to_backend(measurement_reading, i)

                remaining_time = settings.read_interval_s - (
                    time.time_ns() - start_time
                ) / 1e9
                if remaining_time > 0:
                    time.sleep(remaining_time)  # Delay for the specified interval

    except Exception as e:
        # Log any exceptions that occur during the main loop
        logging.error("An error occurred: %s", str(e))

    finally:
        # Ensure the serial port is closed when the program exits
        logging.info("Serial port closed. Exiting...")


if __name__ == "__main__":
    main()
