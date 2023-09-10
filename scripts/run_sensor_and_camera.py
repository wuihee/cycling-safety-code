import os

from traffic_data_sensors.sensors.depthai_camera import CameraWithSensor
from traffic_data_sensors.utils import cd_to_parent_dir, wait_for_internet

cd_to_parent_dir()
os.chdir("../..")

xml_path = "./yolo/yolov6t_coco_416x416.xml"
bin_path = "./yolo/yolov6t_coco_416x416.bin"

wait_for_internet()

camera = CameraWithSensor(xml_path, bin_path)
camera.process()
