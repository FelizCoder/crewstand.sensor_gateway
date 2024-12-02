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
  - [Sensor Connections](#sensor-connections)
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
    - Configure settings such as the serial port, baud rate, backend URL, read interval, and number of sensors.

    | Environment Variable | Description                         | Example Value                   |
    |----------------------|-------------------------------------|---------------------------------|
    | `backend_sensor_url` | URL of the backend server           | `http://172.17.0.1:5000`        |
    | `read_interval_s`    | Interval between reads in seconds   | `0.5`                           |
    | `sensor_count`       | Number of sensors to read. 1 or 2   | `2`                             |
    | `serial_baud_rate`   | Baud rate for serial communication  | `250000`                        |
    | `serial_port`        | Serial port to connect to           | `"/dev/ttyACM0"`                |

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

## Sensor Connections
The Raspberry Pi Pico uses its ADC pins to read sensor values. Ensure the following connections:

- Sensor 0: Connect to ADC 0 (GPIO 26)
- Sensor 1: Connect to ADC 1 (GPIO 27)
- Ground Reference: Connect ADC 2 (GPIO 28) to Ground

## Firmware Details

The Pico firmware, written in C, includes the following components:

- **Initialization**: Sets up the ADC on the Raspberry Pi Pico for reading sensor values.
- **Commands**: The firmware listens for specific commands sent from the host script to read sensor values.
  - `'0'`: Reads sensor 0.
  - `'1'`: Reads sensor 1.
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
