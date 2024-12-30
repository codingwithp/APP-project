import cv2

# Open camera
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("Error: Could not open the camera.")
else:
    print("Camera is working! Press 'Q' to exit.")

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Error: Could not read from the camera.")
        break
    
    cv2.imshow("Camera Test", frame)
    
    # Close the window when 'Q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
