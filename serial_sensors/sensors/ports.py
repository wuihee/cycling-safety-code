from serial.tools import list_ports
from serial.tools.list_ports_common import ListPortInfo


def find_laser_port() -> str:
    ports = list(list_ports.comports())
    for port in ports:
        if _is_laser_port(port):
            return port.name


def _is_laser_port(port: ListPortInfo) -> bool:
    return "CH340" in port.description
