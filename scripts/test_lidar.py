import os

from traffic_data_sensors.aws_iot.publish import Publisher
from traffic_data_sensors.sensors.lidar_lite_v4 import LidarLiteV4
from traffic_data_sensors.utils import wait_for_internet

os.chdir("..")


wait_for_internet()

publisher = Publisher()

try:
    sensor = LidarLiteV4()
except OSError:
    publisher.publish("Could not connect to sensor.")
    exit()

while True:
    data = sensor.get_data()
    publisher.publish(data)
    print(data)
