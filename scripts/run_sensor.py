from traffic_data_sensors.aws_iot.publish import Publisher
from traffic_data_sensors.sensors.serial.jrt_laser import LaserSensor
from traffic_data_sensors.utils import (
    cd_to_parent_dir,
    wait_for_internet,
    write_to_file,
)

cd_to_parent_dir()
wait_for_internet()

publisher = Publisher()
sensor = LaserSensor()

while True:
    data = sensor.get_data()
    publisher.publish(data)
    write_to_file("../saved_data.txt", data)
    print(data)
