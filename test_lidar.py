from src.aws_iot.publish import Publisher
from src.sensors.lidar_lite_v4 import LidarLiteV4
from src.utils import cd_to_parent_dir, wait_for_internet
import os

cd_to_parent_dir()
os.chdir("..")

wait_for_internet()

publisher = Publisher()
sensor = LidarLiteV4()

while True:
    data = sensor.get_data()
    publisher.publish(data)
    print(data)
