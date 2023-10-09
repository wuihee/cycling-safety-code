from ..base import SerialSensor


class UltrasonicSensor(SerialSensor):
    def __init__(self) -> None:
        super().__init__("/dev/ttyS0", 9600)

    def get_data(self) -> str:
        """
        Get data in a consistent format to be published to MQTT.

        Returns:
            str: Formatted data consisting of the time and distance.
        """
        distance = self.get_distance()
        return f"{self.current_time} {distance} -1"

    def get_distance(self) -> int:
        """
        Measure the current distance with the ultrasonic sensor.

        Returns:
            int: distance in mm.
        """
        protocol = self._read_distance_protocol()
        if not self._is_valid_protocol(protocol):
            return -1

        return self._get_distance_from_protocol(protocol)

    def _read_distance_protocol(self) -> list[int]:
        """
        Read the protocol created by measuring distance, which is 4 bytes long.

        Returns:
            list[int]: An array of decimals representing the respective bytes.
        """
        return self._read_protocol(4)

    def _is_valid_protocol(self, protocol: list[int]) -> bool:
        """
        Determine if the protocol is valid.

        Args:
            protocol (list[int]): The protocol of data from the sensor.

        Returns:
            bool: True if protocol is valid else false.
        """
        if not protocol or len(protocol) != 4:
            return False

        checksum = (protocol[0] + protocol[1] + protocol[2]) & 0x00FF
        return checksum == protocol[3]

    def _get_distance_from_protocol(self, protocol: list[int]) -> int:
        """
        Extract distance from the protocol.

        Args:
            protocol (list[int]): The protocol of data from the sensor.

        Returns:
            int: Distance in mm.
        """
        return (protocol[1] << 8) + protocol[2]
