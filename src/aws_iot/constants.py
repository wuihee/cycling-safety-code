import pathlib


class AWSConstants:
    ENDPOINT = "a1cqysdrxx4ce4-ats.iot.ap-southeast-2.amazonaws.com"
    PORT = 8883
    CLIENT_ID = "tof_sensor"
    TOPIC = "TOF"
    AWS_CERTIFICATE = pathlib.Path("./certs/device.pem.crt")
    AWS_PRIVATE_KEY = pathlib.Path("./certs/private.pem.key")
    AWS_ROOT_CA = pathlib.Path("./certs/Amazon-root-CA-1.pem")
