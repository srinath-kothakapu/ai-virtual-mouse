import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Could not open the default camera.")

try:
    while True:
        success, img = cap.read()
        if not success:
            raise RuntimeError("Could not read a frame from the camera.")

        cv2.imshow("Camera Test", img)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()