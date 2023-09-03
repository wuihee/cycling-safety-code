import paho.mqtt.client as mqtt

from ..utils import write_to_file
from .constants import AWSConstants


class Subscriber:
    def __init__(self):
        """
        Initializes the MQTT client to listen for messages.
        """
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_subscribe = self._on_subscribe

        self.client.tls_set(
            AWSConstants.AWS_ROOT_CA,
            certfile=AWSConstants.AWS_CERTIFICATE,
            keyfile=AWSConstants.AWS_PRIVATE_KEY,
        )

    def subscribe(self):
        """
        Starts the subscription to continually receive messages from MQTT.
        """
        self.client.connect(AWSConstants.ENDPOINT, AWSConstants.PORT, keepalive=60)
        self.client.loop_forever()

    def _on_connect(self, client, userdata, flags, rc) -> None:
        """
        Callback function for when client receives a CONNACK response from the server.
        """
        print(f"Connected with result code {rc}")
        client.subscribe(AWSConstants.TOPIC)

    def _on_message(self, client, userdata, msg) -> None:
        """
        Callback for when a PUBLISH message is received from the server.
        """
        distance = self._decode_message(msg.payload)
        print(distance)
        write_to_file("../tof_data.txt", distance)

    def _on_subscribe(self, client, userdata, mid, granted_qos) -> None:
        """
        Callback function when successfully subscribed.
        """
        print(f"Subscribed to topic {AWSConstants.TOPIC} successfully")

    def _decode_message(self, message: str) -> int:
        """
        Decode message received from MQTT.

        Args:
            message (str): Message received.

        Returns:
            int: The distance incidicated in the message.
        """
        message = message.decode()
        message = message.strip('"')
        return message
