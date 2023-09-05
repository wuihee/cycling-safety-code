import datetime
import time

import smbus2


class LidarLiteV4:
    def __init__(self, address=0x62):
        """
        Initializes the LIDAR-Lite sensor interface.

        Args:
            address (hexadecimal, optional): I2C address of the sensor. Defaults to 0x62.
        """
        self.bus = smbus2.SMBus(1)
        self.address = address
        self.distance_register = 0x00
        self.distance_write_value = 0x04

    @property
    def current_time(self) -> str:
        """
        Returns the current time.

        Returns:
            str: Format is HH:MM:SS
        """
        t = str(datetime.datetime.now())
        return t.split(" ")[1].split(".")[0]

    def get_data(self) -> str:
        """
        Get data in a consistent format to be published to MQTT.

        Returns:
            str: Formatted data consisting of the time, distance and signal strength.
        """
        distance = self.get_distance()
        return f"{self.current_time} {distance} -1"

    def get_distance(self) -> int:
        """
        Returns the distance measured in millimeters.

        Returns:
            int: Distance.
        """
        self._write(self.distance_register, self.distance_write_value)
        return self._read_distance() * 10

    def _write(self, register, value) -> None:
        """
        Write a byte to a give register.

        Args:
            register (_type_): Register address to write to.
            value (_type_): Byte value to write.
        """
        self.bus.write_byte_data(self.address, register, value)
        time.sleep(0.02)

    def _read_distance(self):
        """
        Read and return the measured distance from the sensor.

        Returns:
            _type_: Measured distance in centimeters.
        """
        high_byte = self.bus.read_byte_data(self.address, 0x10)
        low_byte = self.bus.read_byte_data(self.address, 0x11)
        return (low_byte << 8) + high_byte


if __name__ == "__main__":
    lidar = LidarLiteV4()
    print(lidar.get_distance())
