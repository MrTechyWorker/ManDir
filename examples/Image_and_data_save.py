import cv2
import time
from ManDir import ManDir

# Directory to save images
filemanager = ManDir("captured_imgs", 5)

# Open the webcam
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Could not access the camera.")
    exit()

print("Press 'q' to exit.")

# Start capturing images
try:
    frame_count = 0
    while True:
        # Capture a frame
        ret, frame = camera.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Show the live feed
        cv2.imshow("Live Feed", frame)

        # Save the frame every 5 seconds
        if frame_count % 60 == 0:  # Assuming camera runs at 30 FPS
            timestamp = int(time.time())
            filemanager.save(imgfile=[frame,".jpg"], picklefile=["frame",".sav"])

        frame_count += 1

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Release the camera and close the window
    camera.release()
    cv2.destroyAllWindows()