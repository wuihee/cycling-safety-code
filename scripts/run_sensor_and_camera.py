import os

from cycling_safety.sensors.depthai_camera import CameraWithSensor
from cycling_safety.utils import cd_to_parent_dir, wait_for_internet
from cycling_safety.sensors.lidar_lite_v4 import LidarLiteV4

cd_to_parent_dir()
os.chdir("../..")

sensor = LidarLiteV4()
xml_path = "./yolo/yolov6t_coco_416x416.xml"
bin_path = "./yolo/yolov6t_coco_416x416.bin"

wait_for_internet()

camera = CameraWithSensor(sensor, xml_path, bin_path)
camera.start(show_preview=False)
