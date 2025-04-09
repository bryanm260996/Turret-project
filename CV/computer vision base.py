import cv2  # OpenCV library, must be installed in Python
import depthai as dai  # DepthAI library for OAK cameras

# Create a pipeline for the OAK camera
pipeline = dai.Pipeline()

# Define the OAK camera node
color_camera = pipeline.createColorCamera()
color_camera.setPreviewSize(640, 480)
color_camera.setInterleaved(False)
color_camera.setFps(30)

# Create an output stream
xout_video = pipeline.createXLinkOut()
xout_video.setStreamName("video")
color_camera.preview.link(xout_video.input)

# detect objects:
featureTracker = pipeline.create(dai.node.FeatureTracker)
featureTracker.setHardwareResources(2, 2)
# Specify to wait until configuration message arrives to inputConfig Input.
featureTracker.setWaitForConfigInput(True)



# Connect to the OAK device and start the pipeline
with dai.Device(pipeline) as device:
    print("Connected to OAK Camera")

    # Get the output queue for video frames
    video_queue = device.getOutputQueue(name="video", maxSize=4, blocking=False)

    # Create a display window
    cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
    print("Entering loop")

    while True:
        # Retrieve the frame from the OAK camera
        video_frame = video_queue.get()
        frame = video_frame.getCvFrame()

        # Display the frame
        cv2.imshow("Output", frame)

        # Press 'q' to exit
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    # Release resources
    cv2.destroyAllWindows()
    print("Complete")
