import blobconverter
import cv2
import depthai

from .sensors.laser import LaserSensor
from .utils import write_to_file


class CameraWithSensor:
    def __init__(self, xml_path, bin_path):
        self.sensor = LaserSensor()
        self.labels = {2: "Car", 5: "Bus", 8: "Truck"}
        self.network_path = blobconverter.from_openvino(
            xml=xml_path, bin=bin_path, shaves=6
        )
        self.pipeline = depthai.Pipeline()
        self.setup_pipeline()

    def setup_pipeline(self):
        # Camera Node
        cam_rgb = self.pipeline.createColorCamera()
        cam_rgb.setPreviewSize(416, 416)
        cam_rgb.setResolution(depthai.ColorCameraProperties.SensorResolution.THE_1080_P)
        cam_rgb.setInterleaved(False)
        cam_rgb.setColorOrder(depthai.ColorCameraProperties.ColorOrder.BGR)
        cam_rgb.setFps(40)

        # YOLO Detection Network Node
        detection_network = self.pipeline.createYoloDetectionNetwork()
        detection_network.setBlobPath(self.network_path)
        detection_network.setConfidenceThreshold(0.5)
        detection_network.setNumClasses(80)
        detection_network.setCoordinateSize(4)
        detection_network.setAnchors(
            [10, 14, 23, 27, 37, 58, 81, 82, 135, 169, 344, 319]
        )
        detection_network.setAnchorMasks({"side26": [1, 2, 3], "side13": [3, 4, 5]})
        detection_network.setIouThreshold(0.5)
        detection_network.input.setBlocking(False)

        # Object Tracker Node
        object_tracker = self.pipeline.createObjectTracker()
        object_tracker.setDetectionLabelsToTrack(list(self.labels.keys()))
        object_tracker.setTrackerType(depthai.TrackerType.ZERO_TERM_COLOR_HISTOGRAM)
        object_tracker.setTrackerIdAssignmentPolicy(
            depthai.TrackerIdAssignmentPolicy.SMALLEST_ID
        )

        # Initialize XLinkOut nodes for camera and tracker.
        xout_rgb = self.pipeline.createXLinkOut()
        xout_tracker = self.pipeline.createXLinkOut()

        xout_rgb.setStreamName("preview")
        xout_tracker.setStreamName("tracklets")

        # Linking camera to YOLO.
        cam_rgb.preview.link(detection_network.input)

        # Link NN to tracker.
        detection_network.passthrough.link(object_tracker.inputTrackerFrame)
        detection_network.passthrough.link(object_tracker.inputDetectionFrame)
        detection_network.out.link(object_tracker.inputDetections)

        # Link tracker to computer.
        object_tracker.out.link(xout_tracker.input)
        object_tracker.passthroughTrackerFrame.link(xout_rgb.input)

    def process(self):
        vehicles = set()

        with depthai.Device(self.pipeline) as device:
            preview = device.getOutputQueue("preview", 4, False)
            tracklets = device.getOutputQueue("tracklets", 4, False)
            frame = None

            # Main Loop
            while True:
                img_frame = preview.get()
                track = tracklets.get()

                frame = img_frame.getCvFrame()
                tracklets_data = track.tracklets

                for t in tracklets_data:
                    roi = t.roi.denormalize(frame.shape[1], frame.shape[0])
                    x1 = int(roi.topLeft().x)
                    y1 = int(roi.topLeft().y)
                    x2 = int(roi.bottomRight().x)
                    y2 = int(roi.bottomRight().y)

                    label = self.labels[t.label]
                    vehicle_id = t.id
                    if vehicle_id not in vehicles:
                        distance, _ = self.sensor.measure_distance()
                        vehicles.add(vehicle_id)
                        if distance <= 1500:
                            write_to_file(
                                "./passed_cars.txt",
                                f"{self.sensor.current_time} {distance} {label}",
                            )

                    cv2.putText(
                        frame,
                        str(label),
                        (x1 + 10, y1 + 20),
                        cv2.FONT_HERSHEY_TRIPLEX,
                        0.5,
                        255,
                    )
                    cv2.rectangle(
                        frame, (x1, y1), (x2, y2), (255, 0, 0), cv2.FONT_HERSHEY_SIMPLEX
                    )

                cv2.imshow("tracker", frame)

                if cv2.waitKey(1) == ord("q"):
                    break
