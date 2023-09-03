from src.aws_iot.publish import Publisher
from src.sensors.serial.jrt_laser import LaserSensor
from src.utils import cd_to_parent_dir, wait_for_internet, write_to_file

cd_to_parent_dir()
wait_for_internet()

publisher = Publisher()
sensor = LaserSensor()

while True:
    data = sensor.get_data()
    publisher.publish(data)
    write_to_file("../saved_data.txt", data)
    print(data)
