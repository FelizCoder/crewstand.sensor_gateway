# CrewStand Pico Interface

This repository is a component of the CrewStand project, focused on interfacing with the Raspberry Pi Pico microcontroller to read analog sensor values and communicate them to the CrewStand backend.

- [CrewStand Pico Interface](#crewstand-pico-interface)
  - [Overview](#overview)
  - [Key Features](#key-features)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Flash the Pico Firmware](#flash-the-pico-firmware)
    - [Running with Python](#running-with-python)
    - [Running with Docker](#running-with-docker)
  - [Usage](#usage)
    - [Using the Mock Serial Module](#using-the-mock-serial-module)
  - [Sensor Connections](#sensor-connections)
  - [Defining Sensor Ranges](#defining-sensor-ranges)
    - [Setting Voltage and Measurement Ranges](#setting-voltage-and-measurement-ranges)
    - [Detailed Steps](#detailed-steps)
    - [Example](#example)
    - [Important Notes](#important-notes)
  - [Log Level Configuration](#log-level-configuration)
  - [Firmware Details](#firmware-details)
  - [Example Usage](#example-usage)
  - [Debugging and Logs](#debugging-and-logs)
  - [Troubleshooting](#troubleshooting)

## Overview

The CrewStand Pico Interface repository contains the following components:

- **Pico Firmware:** C code designed to run on the Raspberry Pi Pico. This code handles analog sensor readings and communicates with the host system over a serial connection.
- **Host Script:** A Python script running on the host system (also available as a Docker image) that reads sensor values from the Pico over a serial connection, processes the data, and sends it to the CrewStand backend for further analysis and storage.

## Key Features

1. **Analog Sensor Reading:** Continuously reads analog sensor values using the ADC feature of the Raspberry Pi Pico.
2. **Serial Communication:** Efficient serial communication between the Pico microcontroller and the host system.
3. **Data Handling:** Processes and validates sensor data before sending it to the backend.
4. **Backend Integration:** Seamlessly integrates with the CrewStand backend for data storage and further analysis.
5. **Ground Reference for Offset Correction:** Corrects the sensor reading by taking a ground reference measurement.

## Getting Started

### Prerequisites

- Raspberry Pi Pico
- A host machine with Python 3 installed (if not using Docker)
- Required Python packages (specified in `requirements.txt`, if not using Docker)

### Installation

### Flash the Pico Firmware

- Ensure you have the Pico SDK and toolchain set up on your machine.
- Navigate to the `pico` directory and compile the code:
  ```sh
  mkdir build
  cd build
  cmake ..
  make
  ```
- Follow the instructions to flash the resulting firmware (`adc_console.uf2`) onto your Pico.

### Running with Python

1. **Install Python Dependencies**

   ```sh
   pip install -r requirements.txt
   ```

2. **Edit `.env.example`**
   | Environment Variable | Description | Example Value |
   | -------------------- | ---------------------------------- | ----------------------- |
   | `backend_sensor_url` | URL of the backend server | `http://localhost:5000` |
   | `log_level` | Log level for the application | `INFO` |
   | `measurement_range` | Measurement ranges for sensors | `[[0.0,1.0], [0,100]]` |
   | `read_interval_s` | Interval between reads in seconds | `0.5` |
   | `sensor_count` | Number of sensors to read. 1 or 2 | `2` |
   | `serial_baud_rate` | Baud rate for serial communication | `250000` |
   | `serial_port` | Serial port to connect to | `mock` |
   | `voltage_range` | Voltage range for sensors | `[0,3.3]` |

3. **Start the Host Script**

   ```sh
   python host/main.py
   ```

4. **Monitor Logs**
   - The script logs its operation to the console. It will attempt to read sensor values periodically and send the data to the backend.

### Running with Docker

1. **Pull the Docker Image**

   ```sh
   docker pull ghcr.io/felizcoder/crewstand.sensor_gateway:latest
   ```

2. **Run the Docker Container**

   ```sh
   docker run --rm -it \
       --env-file </path/to/your/.env> \
       -v /dev/serial/by-id/<your-serial-device>:/dev/ttyACM0 \
       --privileged \
       ghcr.io/felizcoder/crewstand.sensor_gateway:latest
   ```

   - Ensure you replace `/path/to/your/.env` with the actual path to your environment file and `/dev/serial/by-id/your-serial-device` with the path to your serial device.

## Usage

- **Commands:**
  - The firmware on the Pico listens for commands to sample sensor data (`'0'` for sensor 0 and `'1'` for sensor 1). These commands are sent by the host script to initiate a reading for the respective sensor.
  - Ground reference is utilized for offset correction before calculating the final sensor value.

### Using the Mock Serial Module

To use the mock serial module, set `serial_port` to `"mock"` in your `.env` file. This will simulate a serial connection and generate mock sensor readings. In this mode, the host script will not attempt to communicate on the serial port. The mock readings are generated based on a sine wave, allowing for a simple demonstration of the sensor gateway's functionality without the need for actual sensor hardware.

**Example `.env` file:**
```plaintext
backend_sensor_url='http://localhost:5000'
log_level='INFO'
measurement_range='[[0.0,1.0], [0,100]]'
read_interval_s='0.5'
sensor_count='2'
serial_baud_rate='250000'
serial_port='mock'
voltage_range='[-1,1]'
```

## Sensor Connections

The Raspberry Pi Pico uses its ADC pins to read sensor values. Ensure the following connections:

- Sensor 0: Connect to ADC 0 (GPIO 26)
- Sensor 1: Connect to ADC 1 (GPIO 27)
- Ground Reference: Connect ADC 2 (GPIO 28) to Ground

## Defining Sensor Ranges

To properly define the measurement ranges for your sensors, you need to specify the voltage range that your sensors operate within and the corresponding measurement ranges. This is essential for accurate data acquisition and interpolation.

### Setting Voltage and Measurement Ranges

1. **Voltage Range:**

   - The voltage range represents the minimum and maximum voltage values that your sensors can output. This range is typically dictated by the specifications of the sensor.

2. **Measurement Range:**

   - The measurement range corresponds to the voltage range and represents the actual measurement values (e.g., flow rate, temperature) that the sensor outputs at the given voltages. Each sensor can have a unique measurement range.

3. **Configuration:**
   - These ranges are defined as environment variables.

- **voltage_range**: e.g. `[0, 3.3]`

  - This means your sensor operates between 0V and 3.3V.

- **measurement_range**: e.g. `[[0.0, 1.0], [0, 100]]`
  - Each list within the main list represents the measurement range for each sensor.
  - `[0.0, 1.0]`: Measurement range for Sensor 0 (e.g., 0V corresponds to 0 units, and 3.3V corresponds to 1 unit).
  - `[0, 100]`: Measurement range for Sensor 1 (e.g., 0V corresponds to 0 units, and 3.3V corresponds to 100 units).

### Detailed Steps

1. **Edit `.env.example`**:

   - Set `voltage_range` to your sensor's voltage range.
   - Set `measurement_range` to a list of measurement ranges corresponding to each sensor.

2. **Verify Configuration**:
   - Ensure that the number of measurement ranges in `measurement_range` matches `sensor_count`.

### Example

For a setup with two sensors:

- Sensor 0 outputs from 0V to 3.3V, and the measurement values range from 0.0 to 1.0 units.
- Sensor 1 outputs from 0V to 3.3V, and the measurement values range from 0 to 100 units.

The `.env` file will include:

```plaintext
voltage_range='[0,3.3]'
measurement_range='[[0.0,1.0], [0,100]]'
```

### Important Notes

- Ensure the `voltage_range` and `measurement_range` reflect the actual operating specifications of your sensors.
- The `measurement_range` must have the same number of entries as the `sensor_count`.

By defining these ranges accurately, you ensure that the host script can correctly interpolate the raw voltage readings into meaningful measurement values, which are then sent to the backend for processing.

## Log Level Configuration

To adjust the log level of the application, you can set the `log_level` environment variable in your `.env` file. The default log level is set to "INFO".

```plaintext
log_level='INFO'
```

## Firmware Details

The Pico firmware, written in C, includes the following components:

- **Initialization**: Sets up the ADC on the Raspberry Pi Pico for reading sensor values.
- **Commands**: The firmware listens for specific commands sent from the host script to read sensor values.
  - `'0'`: Reads sensor 0.
  - `'1'`: Reads sensor 1.
  - `'s'`: Reads all sensors.
- **Sensor Reading with Offset Correction**:
  - For each sensor reading, the ground reference (ADC channel 2) is read to correct any offset before calculating the actual sensor voltage.

## Example Usage

1. **Running with Python**:

   ```sh
   python host/main.py
   ```

   During execution, the host script will periodically request sensor readings and send them to the backend for further processing.

2. **Running with Docker**:
   ```sh
   docker run --rm -it \
       --env-file </path/to/your/.env\
       -v /dev/serial/by-id/<your-serial-device>:/dev/ttyACM0 \
       --privileged \
       ghcr.io/felizcoder/crewstand.sensor_gateway:latest
   ```

## Debugging and Logs

- **Logs**: Monitor the console output for logs. The script logs important steps, including requesting sensor readings, receiving responses, and sending data to the backend.

## Troubleshooting

- **Connection Issues**: Ensure that the serial port specified in your environment file is correct and that the Raspberry Pi Pico is properly connected.
- **Sensor Readings**:
  - If no readings are received, check the connections to your sensors and ensure that the firmware is correctly flashed onto the Pico.
  - Use the command-line interface (`'0'` and `'1'`) to manually request sensor readings for testing.
