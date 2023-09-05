import smbus
import time


class LidarLiteV4:
    def __init__(self, address=0x62):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.distance_register = 0x00
        self.distance_write_value = 0x04
        
    def get_distance(self):
        """Return distance in mm."""
        self._write(self.distance_register, self.distance_write_value)
        return self._read_distance() * 10

    def _write(self, register, value):
        self.bus.write_byte_data(self.address, register, value)
        time.sleep(0.02)

    def _read_distance(self):
        """Return distance in cm."""
        high_byte = self.bus.read_byte_data(self.address, 0x10)
        low_byte = self.bus.read_byte_data(self.address, 0x11)
        return (low_byte << 8) + high_byte


if __name__ == "__main__":
    lidar = LidarLiteV4()
    print(lidar.get_distance())
