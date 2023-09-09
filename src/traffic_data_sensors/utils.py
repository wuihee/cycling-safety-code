import os
import socket
import subprocess
import time


def cd_to_parent_dir() -> None:
    """
    Change the working directory to that of the parent directory.
    """
    os.chdir(os.path.dirname(os.path.realpath(__file__)))


def write_to_file(path: str, message: str, mode="a") -> None:
    """
    Utility function to write message to file.

    Args:
        (str) path: Path to file.
        (str) message: Message to write.
        (str) mode: Mode of writing to file. Default is append.
    """
    with open(path, mode) as file:
        file.write(message + "\n")


def is_internet_available() -> bool:
    """
    Check for internet by tyring to connect to google.com

    Returns:
        bool: Returns true if there is internet else false.
    """
    try:
        socket.create_connection(("www.google.com", 80), timeout=3)
        return True
    except OSError:
        return False


def wait_for_internet() -> None:
    while not is_internet_available():
        time.sleep(1)
        
        
def wait_for_i2c(address, bus=1, timeout=60):
    end_time = time.time() + timeout
    while time.time() < end_time:
        result = subprocess.check_output(["i2cdetect", "-y", str(bus)]).decode("utf-8")
        if str(address) in result:
            return True
        time.sleep(1)
    return False
