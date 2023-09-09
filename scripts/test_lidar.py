import os
import time
import subprocess

from traffic_data_sensors.aws_iot.publish import Publisher
from traffic_data_sensors.sensors.lidar_lite_v4 import LidarLiteV4
from traffic_data_sensors.utils import cd_to_parent_dir, wait_for_internet


def wait_for_i2c(address, bus=1, timeout=60):
    end_time = time.time() + timeout
    while time.time() < end_time:
        result = subprocess.check_output(["i2cdetect", "-y", str(bus)]).decode("utf-8")
        if str(address) in result:
            return True
        time.sleep(1)
    return False


cd_to_parent_dir()
os.chdir("../..")

# wait_for_internet()
wait_for_i2c(62)
print("Connected to internet")

publisher = Publisher()
sensor = LidarLiteV4()

while True:
    try:
        data = sensor.get_data()
        publisher.publish(data)
        print(data)
        time.sleep(0.05)
    except Exception as e:
        wait_for_i2c(62)
