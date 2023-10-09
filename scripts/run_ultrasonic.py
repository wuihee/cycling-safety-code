import os
import time

from cycling_safety.aws_iot import Publisher
from cycling_safety.sensors.serial import UltrasonicSensor
from cycling_safety.utils import cd_to_parent_dir, wait_for_internet

cd_to_parent_dir()
os.chdir("../..")

wait_for_internet()

publisher = Publisher()
sensor = UltrasonicSensor()

while True:
    data = sensor.get_data()
    publisher.publish(data)
    print(data)
