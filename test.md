# Sensors Used

- [TOF Laser Range Sensor by WaveShare](https://www.waveshare.com/tof-laser-range-sensor.htm)
- [Laser Distance Sensor by Chengdu JRT Meter Technology Co. Ltd](https://www.alibaba.com/product-detail/Laser-Distance-Measuring-Device-100m-Chip_1600877291661.html?spm=a2700.shop_plgr.41413.11.4f9474e2pi4SXS)

## Installation

First, clone the repository.

```bash
git clone https://github.com/wuihee/serial-sensors.git
```

Afterwards install the required Python modules.

```bash
pip install -r requirements.txt
```

### Publishing/Subscribing with AWS IOT

When running my sensors on the Raspberry Pi, I published the data collected to AWS IoT's message broker. I could then see the data arriving in real-time on my laptop by subscribing to the message broker.

I have included this optional publish/subscribe functionality in the [`client`](./serial_sensors/client/) module. To use this feature, first install the [AWS IoT Python SDK](https://docs.aws.amazon.com/iot/latest/developerguide/iot-sdks.html). After that, copy the certificates into the [certs](./certs/) folder. Once done, you should be able to publish and subscribe to the message broker.

## Usage

### Sensors

All sensors inherit from a `Sensor` base from [`sensors.py`](./serial_sensors/sensors/sensor.py), which include common methods to read/write data from serial port.

#### WaveShare Time of Flight Sensor

```python
from serial_sensors.sensors.tof import TOFSensor

sensor = TOFSensor()
```

#### Chengdu JRT Laser Distance Sensor

```python
from serial_sensors.sensors.laser import LaserSensor

sensor = LaserSensor()
```

### Get Sensor Data

Get time, distance, and signal strength in a string.

```python
data = sensor.get_data()
```

### Publishing Data

Publish data to AWS IoT message broker.

```python
from serial_sensors.client.publish import Publisher

publisher = Publisher()
data = "data to publish"
publisher.publish(data)
```

### Subscribing

Subscribe to recieve data from AWS IoT message broker. The `subscribe()` method will start a loop which continuously checks for and recieves incoming messages.

```python
from serial_sensors.client.subscribe import Subscriber

subscriber = Subscriber()
subscriber.subscribe()
```

## Todo

- Write tests.
- Test if port works on Raspberry Pi and on TOF sensor.
