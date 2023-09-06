from traffic_data_sensors.sensors.depthai_camera import CameraWithSensor

xml_path = "./yolo/yolov6t_coco_416x416.xml"
bin_path = "./yolo/yolov6t_coco_416x416.bin"

camera = CameraWithSensor(xml_path, bin_path)
camera.process()