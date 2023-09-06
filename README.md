# Traffic Data Collection Sensors

Code to run the sensors and publish/subscribe to AWS IoT message broker in [traffic data analysis project](https://github.com/wuihee/Traffic-Data-Collection/tree/main).

## Table of Contents

1. [Installation & Setup](#installation--setup)
2. [Usage](#usage)

## Installation & Setup

### Dependencies

```bash
pip install -r requirements.txt
```

### Raspberry Pi Autostart on Boot with Systemd

In my experiments, I needed my scripts to autostart on boot on the Raspberry Pi to automatically run the sensors.

#### Automatically Create Service

Automatically create a service that autoruns your script with `create_service.sh`.

First make the script executable.

```bash
chmod +x create_service.sh
```

Run the script and follow the prompts.

```bash
sudo ./create_service.sh
```

#### Manually Create Service

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

### AWS IoT Setup

To use the [`aws_iot`](./src/aws_iot/) module to publish data from sensors to AWS IoT Message Broker, register for AWS IoT core, download the AWS IoT Device Python SDK, and copy and paste the necessary certificates in the certs folder.

## Usage

### Serial Sensor Setup

#### Windows Setup

To use the sensor on Windows with the software provided:

- **Install Drivers**: Install [CP210x USB to UART drivers](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers?tab=downloads) for the sensor to work on Windows.
- **Enable COM Ports**: Windows Device Manager &rarr; Actions &rarr; Add Legacy Hardware &rarr; And installing Ports (COM & LPT).
- **Baud Rate**: Finally, for the sensor to work with the software, make sure the baudrate is correctly set.

#### Raspberry Pi Setup

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
    nano /boot/config.txt
    ```

- Add the following line to the end of the file:

    ```text
    enable_uart=1
    ```

### [WaveShare TOF Sensor](https://www.waveshare.com/tof-laser-range-sensor.htm)

- Follow the [serial sensor setup](#serial-sensor-setup).
- **Baudrate**: 921600

### [JRT BB2X Laser Distance Sensor](https://www.alibaba.com/product-detail/)

- Follow the [serial sensor setup](#serial-sensor-setup).
- **Baudrate**: 115200bps.

### [LIDAR-Lite V4](https://www.sparkfun.com/products/18009)

Install I2C tools.

```bash
sudo apt-get install -y i2c-tools
```

Check to see if sensor is connected to I2C interface. The sensor should be connected at address 0x62.

```bash
i2cdetect -y 1
```

### Subscribe to AWS IoT Message Broker

```python
from src.aws_iot.subscribe import Subscriber

subscriber = Subscriber()
subscriber.subscribe()
```
