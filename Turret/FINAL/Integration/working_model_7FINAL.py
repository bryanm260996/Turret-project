import serial
import cv2
import numpy as np
import onnxruntime as ort
import depthai as dai
from ultralytics.utils import yaml_load
from ultralytics.utils.checks import check_yaml

class YOLOv8:
    def __init__(self, onnx_model, yaml, confidence_thres, iou_thres, serial_port, target_color='yellow'):
        print("Initializing YOLO object")
        self.onnx_model = onnx_model
        self.yaml = yaml
        self.confidence_thres = confidence_thres
        self.iou_thres = iou_thres
        self.target_color = target_color.lower()
        self.classes = yaml_load(check_yaml(self.yaml))["names"]
        self.color_palette = np.random.uniform(0, 255, size=(len(self.classes), 3))
        self.serial_port = serial.Serial(serial_port, baudrate=115200, timeout=0.01)

    def draw_detections(self, img, box, score, class_id, target_index):
        if self.classes[class_id].lower() != self.target_color:
            return

        x1, y1, w, h = box
        color = (0, 0, 255) if self.target_color == 'red' else (255, 0, 0)
        cv2.rectangle(img, (int(x1), int(y1)), (int(x1 + w), int(y1 + h)), color, 2)
        label = f"Target {target_index} ({self.classes[class_id]}): {score:.2f}"
        (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        label_x = x1
        label_y = y1 - 10 if y1 - 10 > label_height else y1 + 10
        cv2.rectangle(img, (label_x, label_y - label_height), (label_x + label_width, label_y + label_height), color, cv2.FILLED)
        cv2.putText(img, label, (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

        cx = int(x1 + w // 2) + 10
        cy = int(y1 + h // 2)
        img_center_x = img.shape[1] // 2
        img_center_y = img.shape[0] // 2
        crosshair_x = cx - img_center_x
        crosshair_y = cy - img_center_y
        cv2.line(img, (cx - 10, cy), (cx + 10, cy), (0, 255, 0), 2)
        cv2.line(img, (cx, cy - 10), (cx, cy + 10), (0, 255, 0), 2)

        print(f"Target {target_index} detected. Crosshair relative position: (X: {crosshair_x-2}, Y: {crosshair_y+2})")

        tx_msg = f'Target {target_index}: {crosshair_x-2},{crosshair_y+2}\n'
        self.serial_port.write(tx_msg.encode())

        height, width = img.shape[:2]
        center_x = width // 2
        center_y = height // 2
        cv2.line(img, (0, center_y), (width, center_y), (0, 0, 0), 1)
        cv2.line(img, (center_x, 0), (center_x, height), (0, 0, 0), 1)

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
                if self.classes[class_id].lower() != self.target_color:
                    continue
                x, y, w, h = outputs[i][0], outputs[i][1], outputs[i][2], outputs[i][3]
                left = int((x - w / 2) * x_factor)
                top = int((y - h / 2) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)

                # Only include boxes with exactly width=22 and height=22
                if 18 <= width <= 26 and 18 <= height <= 26:
                    class_ids.append(class_id)
                    scores.append(max_score)
                    boxes.append([left, top, width, height])

        indices = cv2.dnn.NMSBoxes(boxes, scores, self.confidence_thres, self.iou_thres)

        detections = []
        for i in indices:
            i = i[0] if isinstance(i, (list, tuple, np.ndarray)) else i
            box = boxes[i]
            x1 = box[0]
            detections.append((x1, self.classes[class_ids[i]], box, scores[i], class_ids[i]))

        detections.sort(key=lambda x: x[0])

        self.nn = []
        for target_index, (_, label, box, score, class_id) in enumerate(detections, start=1):
            self.nn.append([label, box, score])
            self.draw_detections(input_image, box, score, class_id, target_index)

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

pipeline = dai.Pipeline()
color_camera = pipeline.createColorCamera()
color_camera.setPreviewSize(640, 480)
color_camera.setInterleaved(False)
color_camera.setFps(30)

xout_video = pipeline.createXLinkOut()
xout_video.setStreamName("video")
color_camera.preview.link(xout_video.input)

with dai.Device(pipeline) as device:
    print("Connected to OAK Camera")
    video_queue = device.getOutputQueue(name="video", maxSize=4, blocking=False)
    cv2.namedWindow("Output", cv2.WINDOW_NORMAL)

    model_path = 'C:/Users/m260996/Documents/AY2025/309/Turret/CV/yolomodel.onnx'
    yaml_path = 'C:/Users/m260996/Documents/AY2025/309/Turret/CV/data.yaml'
    yolo_model = YOLOv8(model_path, yaml_path, confidence_thres=0.38, iou_thres=0.38, serial_port='COM19', target_color='red')

    print("Starting video stream and inference... Press 'q' to quit.")
    while True:
        frame = video_queue.get().getCvFrame()
        detections_frame = yolo_model.CPUinference(frame)
        cv2.imshow("Output", detections_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
