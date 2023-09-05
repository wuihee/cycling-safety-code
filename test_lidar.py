from src.aws_iot.publish import Publisher
from src.sensors.lidar_lite_v4 import LidarLiteV4
from src.utils import wait_for_internet

# wait_for_internet()

publisher = Publisher()
sensor = LidarLiteV4()

while True:
    distance = sensor.get_distance()
    publisher.publish(distance)