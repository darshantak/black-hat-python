import cv2,time

def capture_and_save_photo(count):
    # Open the first camera device (usually the default webcam)
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    time.sleep(2)
    # Capture a single frame from the camera
    ret, frame = cap.read()
    if ret:
        save_path = f"/Users/photo{count}.jpg"
        # Save the captured frame as an image file
        cv2.imwrite(save_path, frame)
        print("Photo captured and saved as 'photo.jpg'.")
    else:
        print("Error: Failed to capture image.")

    # Release the camera
    cap.release()

if __name__ == "__main__":
    count = 1
    while True: 
        capture_and_save_photo(count)
        time.sleep(8)
        count+=1

