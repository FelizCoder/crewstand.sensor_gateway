# CrewStand Pico Interface

This repository is a component of the CrewStand project, focused on interfacing with the Raspberry Pi Pico microcontroller to read analog sensor values and communicate them to the CrewStand backend.

## Overview

The CrewStand Pico Interface repository contains the following components:
- **Pico Firmware:** C code designed to run on the Raspberry Pi Pico. This code handles analog sensor readings and communicates with the host system over a serial connection.
- **Host Script:** A Python script running on the host system (also available as a Docker image) that reads sensor values from the Pico over a serial connection, processes the data, and sends it to the CrewStand backend for further analysis and storage.

## Key Features

1. **Analog Sensor Reading:** Continuously reads analog sensor values using the ADC feature of the Raspberry Pi Pico.
2. **Serial Communication:** Efficient serial communication between the Pico microcontroller and the host system.
3. **Data Handling:** Processes and validates sensor data before sending it to the backend.
4. **Backend Integration:** Seamlessly integrates with the CrewStand backend for data storage and further analysis.

## Getting Started

### Prerequisites

- Raspberry Pi Pico
- A host machine with Python 3 installed (if not using Docker)
- Required Python packages (specified in `requirements.txt`, if not using Docker)

### Installation

2. **Flash the Pico Firmware**
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
    - Configure settings such as the serial port, baud rate, backend URL, and read interval.

    | Environment Variable | Description                         | Example Value         |
    |----------------------|-------------------------------------|-----------------------|
    | `read_interval_s`    | Interval between reads in seconds   | `0.5`                 |
    | `serial_port`        | Serial port to connect to           | `"/dev/ttyACM0"`      |
    | `serial_baud_rate`   | Baud rate for serial communication  | `250000`              |
    | `backend_url`        | URL of the backend server           | `http://localhost:5000/sensor/reading`|

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

   - Ensure you replace `/path/to/your/.env` with the actual path to your enviroment file and `/dev/serial/by-id/your-serial-device` with the path to your serial device.

## Usage

- **Commands:**
  - The firmware on the Pico listens for a command to sample sensor data (`'s'`). This command is sent by the host script to initiate a reading.
