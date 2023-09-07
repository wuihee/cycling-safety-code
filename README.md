# Traffic Data Sensors

Code to run the sensors and publish/subscribe to AWS IoT message broker in [traffic data analysis project](https://github.com/wuihee/Traffic-Data-Collection/tree/main).

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Raspberry Pi Autostart Setup](#raspberry-pi-autostart-setup)
4. [AWS IoT Setup](#aws-iot-setup)

## Installation

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Build Package

```bash
python setup.py bdist_wheel sdist
```

### Install Package Locally

This will allow you to run .py files in [scripts](./scripts/) locally.

```bash
pip install -e .
```

## Usage

**IMPORTANT: To ensure good connectivity to the Raspberry Pi, make sure the Raspberry Pi is connected to a 5V power source and if using USB cables, make sure that they are USB 2.0.**

### Serial Sensor Setup

#### Windows Setup

To use the sensor on Windows with the software provided:

- **Install Drivers**: Install [CP210x USB to UART drivers](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers?tab=downloads) for the sensor to work on Windows.
- **Enable COM Ports**: Windows Device Manager &rarr; Actions &rarr; Add Legacy Hardware &rarr; And installing Ports (COM & LPT).
- **Baud Rate**: Finally, for the sensor to work with the software, make sure the baudrate is correctly set.

#### Raspberry Pi UART Setup

To use the sensor on the Raspberry Pi:

- **Enable Serial Port Settings**: Enter the following command in the terminal:

    ```bash
    sudo raspi-config
    ```

- Interfaces Options &rarr; Serial Port
  - Would you like a login shell to be accessible over serial? &rarr; No
  - Would you like serial port hardware to be enabled &rarr; Yes
- **Enable UART**: Open `/boot/config.txt`:

    ```bash
    sudo nano /boot/config.txt
    ```

- Make sure the following line is in the file:

    ```text
    enable_uart=1
    ```

### [WaveShare TOF Sensor](https://www.waveshare.com/tof-laser-range-sensor.htm)

- Follow the [serial sensor setup](#serial-sensor-setup).
- **Baudrate**: 921600bps

#### TOF Sensor Code

```python
from traffic_data_sensors.sensors.serial.waveshare_tof import TOFSensor

sensor = TOFSensor()
sensor.get_data()
```

### [JRT BB2X Laser Distance Sensor](https://www.alibaba.com/product-detail/)

- Follow the [serial sensor setup](#serial-sensor-setup).
- **Baudrate**: 115200bps.

#### Laser Sensor Code

```python
from traffic_data_sensors.sensors.serial.jrt_laser import LaserSensor

sensor = LaserSensor()
sensor.get_data()
```

### [LIDAR-Lite V4](https://www.sparkfun.com/products/18009)

#### Raspberry Pi I2C Setup

- **Enable I2C Settings**: Enter the following command in the terminal:

    ```bash
    sudo raspi-config
    ```

- Interfaces Options &rarr; I2C
  - Would you like ARM I2C interface to be enabled? &rarr; Yes
  - Would you like the I2C kernel module to be loaded by default? &rarr; Yes
- **I2C Command Line Tools**:

    ```bash
    sudo apt-get install -y i2c-tools
    ```

- Check to see if sensor is connected to I2C interface. The sensor should be connected at address 0x62.

    ```bash
    i2cdetect -y 1
    ```

- **Enable I2C**: Open `/boot/config.txt`:

    ```bash
    sudo nano /boot/config.txt
    ```

- Make sure the following line is in the file:

    ```text
    enable_uart=1
    ```

#### LIDAR Sensor Code

```python
from traffic_data_sensors.sensors.lidar_lite_v4 import LidarLiteV4

sensor = LidarLiteV4()
sensor.get_data()
```

### Publish to AWS IoT Message Broker

```python
from serial_sensors.client.publish import Publisher

publisher = Publisher()
data = "data to publish"
publisher.publish(data)
```

### Subscribe to AWS IoT Message Broker

```python
from traffic_data_sensors.aws_iot.subscribe import Subscriber

subscriber = Subscriber()
subscriber.subscribe()
```

## Raspberry Pi Autostart Setup

In my experiments, I needed my scripts to autostart on boot on the Raspberry Pi to automatically run the sensors.

### Automatically Create Service

Automatically create a service that autoruns your script with [`create_service.sh`](./scripts/create_service.sh).

First make the script executable.

```bash
chmod +x create_service.sh
```

Run the script and follow the prompts.

```bash
sudo ./create_service.sh
```

### Manually Create Service

Create a service in `/usr/lib/systemd/system`. E.g. `sensor.service`.

- Include the path to your script in ExecStart.
- Replace `YOUR_USER` with the output of command `whoami`.

```text
[Service]
ExecStart=/usr/bin/python3 /PATH_TO_YOUR_SCRIPT.py
User=YOUR_USER

[Install]
WantedBy=multi-user.target
```

Afterwards reload systemd.

```bash
sudo systemctl daemon-reload
```

Enable your service. Afterwards, your script should autostart on boot.

```bash
sudo systemctl enable SERVICE_NAME.service
```

To disable your service:

```bash
sudo systemctl disable SERVICE_NAME.service
```

To check the status of your service for degbugging:

```bash
sudo systemctl status SERVICE_NAME.service
```

## AWS IoT Setup

To use the [`aws_iot`](./src/aws_iot/) module to publish data from sensors to AWS IoT Message Broker, register for AWS IoT core, download the AWS IoT Device Python SDK, and copy and paste the necessary certificates in the certs folder.
