import subprocess
import time

from traffic_data_sensors.aws_iot.publish import Publisher
from traffic_data_sensors.sensors.lidar_lite_v4 import LidarLiteV4
from traffic_data_sensors.utils import wait_for_internet


def wait_for_i2c_device(address, bus=1, timeout=60):
    end_time = time.time() + timeout
    while time.time() < end_time:
        result = subprocess.check_output(["i2cdetect", "-y", str(bus)]).decode("utf-8")
        if address in result:
            return True
        time.sleep(1)
    return False


wait_for_internet()

publisher = Publisher()

if not wait_for_i2c_device("62"):
    publisher.publish("Couldn't Connect")
    exit()

sensor = LidarLiteV4()

while True:
    data = sensor.get_data()
    publisher.publish(data)
    print(data)
