import cv2  # OpenCV library, must be installed in Python
import depthai as dai  # DepthAI library for OAK cameras
import numpy as np  # For numerical operations

# Create a pipeline for the OAK camera
pipeline = dai.Pipeline()
crosshairs= True
# Define the OAK camera node correctly
color_camera = pipeline.create(dai.node.ColorCamera)
color_camera.setPreviewSize(640, 480)
color_camera.setInterleaved(False)
color_camera.setFps(30)

# Create an output stream
xout_video = pipeline.create(dai.node.XLinkOut)
xout_video.setStreamName("video")
color_camera.preview.link(xout_video.input)

# Connect to the OAK device and start the pipeline
with dai.Device(pipeline) as device:
    print("Connected to OAK Camera")

    # Get the output queue for video frames
    video_queue = device.getOutputQueue(name="video", maxSize=4, blocking=False)

    # Create display windows
    cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)
    print("Entering loop")

    while True:
        # Retrieve the frame from the OAK camera
        video_frame = video_queue.get()
        if video_frame is None:
            print("Warning: No frame received!")
            continue

        frame = video_frame.getCvFrame()

        # Convert the frame to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define the yellow color range (tweak these values if necessary)
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])

        # Create a mask for yellow objects
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Apply Gaussian blur to the mask (optional, helps reduce noise)
        blurred_mask = cv2.GaussianBlur(mask, (9, 9), 2)

        # Find contours in the mask
        contours, _ = cv2.findContours(blurred_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Iterate over contours and look for circles
        for contour in contours:
            # Approximate contour to circle
            ((x, y), radius) = cv2.minEnclosingCircle(contour)

            # Filter out small contours (noise)
            if radius > 10:  # adjust size threshold as needed
                # Draw the circle on the original frame
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
                cv2.putText(frame, f"Target at ({int(x)}, {int(y)})", (int(x) - 50, int(y) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # --- Place turret control code here ---
                # You can use (x, y) to control turret movement!
                print(f"Detected target at X: {int(x)}, Y: {int(y)}")

        # Display the frame with detections
        cv2.imshow("Output", frame)
        cv2.imshow("Mask", mask)  # Optional: show the mask to debug detection

        # Press 'q' to exit
        key = cv2.waitKey(1)
        if key == ord('q'):
            print("Exiting loop")
            break

    # Release resources
    cv2.destroyAllWindows()
    cv2.waitKey(1)  # Ensure windows are closed properly
    print("Complete")
