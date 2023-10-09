import smbus2

from .sensor_base import Sensor


class I2CSensor(Sensor):
    def __init__(self, bus_number=1, address=0x00) -> None:
        """
        Initializes the I2C interface.

        Args:
            bus_number (int, optional): I2C bus number. Defaults to 1.
            address (hexadecimal, optional): I2C address of the sensor. Defaults to 0x00.
        """
        self.bus = smbus2.SMBus(bus_number)
        self.address = address

    def get_data(self) -> None:
        pass

    def get_distance(self) -> None:
        pass

    def _write_byte(self, register: int, value: int) -> None:
        """
        Write a byte to a given register.

        Args:
            register (int): Register address to write to.
            value (int): Byte value to write.
        """
        self.bus.write_byte_data(self.address, register, value)

    def _read_byte(self, register: int) -> int:
        """
        Read a byte from a given register.

        Args:
            register (int): Register address to read from.

        Returns:
            int: The byte value read.
        """
        return self.bus.read_byte_data(self.address, register)

    def _read_16bit_value(self, high_byte_register: int, low_byte_register: int) -> int:
        """
        Read a 16-bit value from two given consecutive registers.

        Args:
            high_byte_register (int): Register address for the high byte.
            low_byte_register (int): Register address for the low byte.

        Returns:
            int: 16-bit value composed of the two bytes.
        """
        high_byte = self.read_byte(high_byte_register)
        low_byte = self.read_byte(low_byte_register)
        return (low_byte << 8) + high_byte
