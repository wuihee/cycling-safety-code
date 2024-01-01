# Traffic Data Sensors

Code to run the sensors and publish/subscribe to AWS IoT message broker in [traffic data analysis project](https://github.com/wuihee/Traffic-Data-Collection/tree/main).

## To Replicate

1. Follow [installation](#installation) instructions.
2. Follow [autostart](#raspberry-pi-autostart-setup) instructions where the script to autostart is [run_sensor_and_camera.py](./scripts/run_sensor_and_camera.py).
3. Ensure that the Raspberry Pi is connected to a LiDAR sensor and the depthAI camera.

## Table of Contents

1. [Installation](#installation)
2. [Sensors](#sensors)
3. [Sensor Setup](#sensor-setup)
4. [AWS IoT Setup](#aws-iot-setup)
5. [Raspberry Pi Autostart Setup](#raspberry-pi-autostart-setup)
6. [API](#api)

## Installation

### Clone the Repository

```bash
git clone https://github.com/wuihee/cycling-safety-code.git
cd cycling-safety-code
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Build Package

```bash
python setup.py bdist_wheel sdist
```

### Install Package Locally

This will allow you to import `traffic_data_sensors` and run .py files in [scripts](./scripts/) locally.

```bash
pip install .
```

## Sensors

- [WaveShare TOF Sensor](https://www.waveshare.com/tof-laser-range-sensor.htm) (**Baudrate**: 921600bps)
- [JRT BB2X Laser Distance Sensor](https://www.alibaba.com/product-detail/JRT-Laser-Distance-Module-High-Accuracy_1600935670921.html?spm=a2700.galleryofferlist.p_offer.d_price.386f1f20EnJdbn&s=p) (**Baudrate**: 115200bps)
- [Garmin LIDAR-Lite V4](https://www.sparkfun.com/products/18009)
- [DFRobot A02YYUW Ultrasonic Sensor](https://www.dfrobot.com/product-1935.html)

## Sensor Setup

**IMPORTANT: To ensure good connectivity to the Raspberry Pi, make sure the Raspberry Pi is connected to a 5V power source and if using USB cables, make sure that they are USB 2.0.**

### Serial Setup

#### Using Serial Sensors with Windows

To use the sensor on Windows with the software provided:

- **Install Drivers**: Install [CP210x USB to UART drivers](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers?tab=downloads) for the sensor to work on Windows.
- **Enable COM Ports**: Windows Device Manager &rarr; Actions &rarr; Add Legacy Hardware &rarr; And installing Ports (COM & LPT).
- **Baud Rate**: Finally, for the sensor to work with the software, make sure the baudrate is correctly set.

#### Using Serial Sensors with Raspberry Pi

To use the sensor on the Raspberry Pi:

1. **Enable Serial Port Settings**: Enter the following command in the terminal:

    ```bash
    sudo raspi-config
    ```

    Interfaces Options &rarr; Serial Port
    - Would you like a login shell to be accessible over serial? &rarr; No
    - Would you like serial port hardware to be enabled &rarr; Yes
2. **Enable UART**: Open `/boot/config.txt`:

    ```bash
    sudo nano /boot/config.txt
    ```

    Make sure the following line is in the file:

    ```text
    enable_uart=1
    ```

### I2C Setup

#### Using I2C Sensors with Raspberry Pi

1. **Enable I2C Settings**: Enter the following command in the terminal:

    ```bash
    sudo raspi-config
    ```

    Interfaces Options &rarr; I2C
   - Would you like ARM I2C interface to be enabled? &rarr; Yes
   - Would you like the I2C kernel module to be loaded by default? &rarr; Yes
2. **I2C Bus Speed**: It is importatnt to set the correct bus speed so the I2C connection remains stable. First, open `/boot/config.txt`:
  
    ```bash
    sudo nano /boot/config.txt
    ```

    This line should already exist, meaning I2C is enabled:

    ```bash
    dtparam=i2c_arm=on
    ```

    To adjust the bus speed:

    ```bash
    i2c_arm_baudrate=100000
    ```

3. **I2C Command Line Tools**:

    ```bash
    sudo apt-get install -y i2c-tools
    ```

    Check to see if sensor is connected to I2C interface. The sensor should be connected at address 0x62.

    ```bash
    i2cdetect -y 1
    ```

## AWS IoT Setup

To use the [`aws_iot`](./src/aws_iot/) module to publish data from sensors to AWS IoT Message Broker, register for AWS IoT core, download the AWS IoT Device Python SDK, and copy and paste the necessary certificates in the certs folder.

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

Create a service (i.e. create a new file ending in .service) in `/usr/lib/systemd/system`. E.g. `sensor.service`.

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

To stop your service:

```bash
sudo systemctl stop SERVICE_NAME.service
```

## API

### Publish to AWS IoT Message Broker

```python
from cycling_safety.aws_iot import Publisher

publisher = Publisher()
data = "data to publish"
publisher.publish(data)
```

### Subscribe to AWS IoT Message Broker

```python
from cycling_safety.aws_iot import Subscriber

subscriber = Subscriber()
subscriber.subscribe()
```

### Using a Sensor

```python
# Importing sensors.
from cycling_safety.sensors.serial import LaserBB2XSensor
from cycling_safety.sensors.serial import LaserTOFSensor
from cycling_safety.sensors.serial import UltrasonicSensor
from cycling_safety.sensors.i2c import LIDARLiteV4

# Intializing sensor object.
sensor = LaserTOFSensor()

# Getting data.
sensor.get_data()
```

### Running DepthAI Camera

```python
from cycling_safety.camera import CameraWithSensor

camera_with_sensor = CameraWithSensor
camera_with_sensor.start()
```
