import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open the default camera.")

    try:
        with mp_hands.Hands() as hand_detector:
            while True:
                success, img = cap.read()
                if not success:
                    raise RuntimeError("Could not read a frame from the camera.")

                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                results = hand_detector.process(img_rgb)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_draw.draw_landmarks(
                            img,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                        )

                cv2.imshow("Hand Tracking", img)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()