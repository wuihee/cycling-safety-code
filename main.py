from serial_sensors.client.publish import Publisher
from serial_sensors.sensors.laser import LaserSensor
from serial_sensors.utils import cd_to_parent_dir, wait_for_internet, write_to_file

cd_to_parent_dir()
wait_for_internet()

publisher = Publisher()
sensor = LaserSensor()

while True:
    data = sensor.get_data()
    publisher.publish(data)
    write_to_file("./files/saved_data.txt", data)
    print(data)
