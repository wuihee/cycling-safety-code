from ..base import I2CSensor


class LIDARLiteV4(I2CSensor):
    def __init__(self, address=0x62):
        """
        Initializes the LIDAR-Lite sensor interface.

        Args:
            address (hexadecimal, optional): I2C address of the sensor. Defaults to 0x62.
        """
        super().__init__(address=address)
        self.distance_register = 0x00
        self.distance_write_value = 0x04

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
        self._write_byte(self.distance_register, self.distance_write_value)
        return self._read_16bit_value(0x10, 0x11) * 10
