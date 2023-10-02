import os
import time

from cycling_safety.aws_iot import Publisher
from cycling_safety.sensors.i2c import LIDARLiteV4
from cycling_safety.utils import cd_to_parent_dir, wait_for_i2c, wait_for_internet

cd_to_parent_dir()
os.chdir("../..")

wait_for_internet()
wait_for_i2c(62)
print("Connected to internet")

publisher = Publisher()
sensor = LIDARLiteV4()
error_count = 0

while True:
    try:
        data = sensor.get_data()
        publisher.publish(data)
        print(data)
        time.sleep(0.02)
    except OSError:
        error_count += 1
        print(error_count)
        wait_for_i2c(62, timeout=1)
    except Exception as e:
        print(f"Waiting for internet {e}")
        wait_for_internet()
