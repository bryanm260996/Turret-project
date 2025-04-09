# EW309 YOLOv8 implementation derived from Ultralytics YOLO 🚀, AGPL-3.0 license
# Performs inference on CPU with DepthAI OAK Camera input
# P. Frontera, March 2024

import cv2
import numpy as np
import onnxruntime as ort
import depthai as dai
from ultralytics.utils import yaml_load
from ultralytics.utils.checks import check_yaml


class YOLOv8:
    """YOLOv8 object detection model class for handling inference and visualization."""

    def __init__(self, onnx_model, yaml, confidence_thres, iou_thres):
        print("Initializing YOLO object")
        self.onnx_model = onnx_model        
        self.yaml = yaml
        self.confidence_thres = confidence_thres
        self.iou_thres = iou_thres

        # Load the class names from the yaml file
        self.classes = yaml_load(check_yaml(self.yaml))["names"]

        # Generate a color palette for the classes
        self.color_palette = np.random.uniform(0, 255, size=(len(self.classes), 3))

    def draw_detections(self, img, box, score, class_id):
        x1, y1, w, h = box
        color = self.color_palette[class_id]
        cv2.rectangle(img, (int(x1), int(y1)), (int(x1 + w), int(y1 + h)), color, 2)
        label = f"{self.classes[class_id]}: {score:.2f}"
        (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        label_x = x1
        label_y = y1 - 10 if y1 - 10 > label_height else y1 + 10
        cv2.rectangle(img, (label_x, label_y - label_height), (label_x + label_width, label_y + label_height), color, cv2.FILLED)
        cv2.putText(img, label, (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    def preprocess(self, frame):
        self.img = frame
        self.img_height, self.img_width = self.img.shape[:2]
        img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (self.input_width, self.input_height))
        image_data = np.array(img) / 255.0
        image_data = np.transpose(image_data, (2, 0, 1))
        image_data = np.expand_dims(image_data, axis=0).astype(np.float32)
        return image_data

    def postprocess(self, input_image, output):
        outputs = np.transpose(np.squeeze(output[0]))
        rows = outputs.shape[0]
        boxes, scores, class_ids = [], [], []
        x_factor = self.img_width / self.input_width
        y_factor = self.img_height / self.input_height

        for i in range(rows):
            classes_scores = outputs[i][4:]
            max_score = np.amax(classes_scores)
            if max_score >= self.confidence_thres:
                class_id = np.argmax(classes_scores)
                x, y, w, h = outputs[i][0], outputs[i][1], outputs[i][2], outputs[i][3]
                left = int((x - w / 2) * x_factor)
                top = int((y - h / 2) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)
                class_ids.append(class_id)
                scores.append(max_score)
                boxes.append([left, top, width, height])

        indices = cv2.dnn.NMSBoxes(boxes, scores, self.confidence_thres, self.iou_thres)
        self.nn = []

        for i in indices:
            box = boxes[i]
            score = scores[i]
            class_id = class_ids[i]
            self.nn.append([self.classes[class_id], box, score])
            self.draw_detections(input_image, box, score, class_id)

        return input_image

    def CPUinference(self, frame):
        session = ort.InferenceSession(self.onnx_model, providers=["CPUExecutionProvider"])
        model_inputs = session.get_inputs()
        input_shape = model_inputs[0].shape
        self.input_width = input_shape[2]
        self.input_height = input_shape[3]
        img_data = self.preprocess(frame)
        outputs = session.run(None, {model_inputs[0].name: img_data})
        output_image = self.postprocess(self.img, outputs)
        return output_image


# ---------------------- OAK Camera Integration ----------------------

# Create a pipeline
pipeline = dai.Pipeline()
color_camera = pipeline.createColorCamera()
color_camera.setPreviewSize(640, 480)
color_camera.setInterleaved(False)
color_camera.setFps(30)

xout_video = pipeline.createXLinkOut()
xout_video.setStreamName("video")
color_camera.preview.link(xout_video.input)

# Connect to the OAK device
with dai.Device(pipeline) as device:
    print("Connected to OAK Camera")

    video_queue = device.getOutputQueue(name="video", maxSize=4, blocking=False)
    cv2.namedWindow("Output", cv2.WINDOW_NORMAL)

    # Initialize YOLO model
    model_path = 'C:/Users/m260996/Documents/AY2025/309/Turret/CV/yolomodel.onnx'
    yaml_path = 'C:/Users/m260996/Documents/AY2025/309/Turret/CV/data.yaml'
    yolo_model = YOLOv8(model_path, yaml_path, confidence_thres=0.25, iou_thres=0.45)

    print("Starting video stream and inference... Press 'q' to quit.")
    while True:
        frame = video_queue.get().getCvFrame()
        detections_frame = yolo_model.CPUinference(frame)
        cv2.imshow("Output", detections_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
