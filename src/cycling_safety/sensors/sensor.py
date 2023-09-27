import datetime
from abc import ABC, abstractclassmethod


class Sensor(ABC):
    @property
    def current_time(self) -> str:
        """
        Returns the current time.

        Returns:
            str: Format is HH:MM:SS
        """
        t = str(datetime.datetime.now())
        return t.split(" ")[1].split(".")[0]

    @abstractclassmethod
    def get_data(self) -> None:
        """
        All distance sensors return data in a consistent format to be published
        to AWS.
        """
        pass

    def get_distance(self) -> None:
        """
        All distance sensors have a method to retrieve the distance.
        """
        pass
