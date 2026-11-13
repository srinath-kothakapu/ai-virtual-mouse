import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


def annotate_frame(hand_detector, img_bgr):
    """Detect hands in a BGR camera frame and draw the landmarks on it.

    Draws in place and returns ``(img_bgr, hand_count)``.
    """
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    results = hand_detector.process(img_rgb)

    hands = results.multi_hand_landmarks or []
    for hand_landmarks in hands:
        mp_draw.draw_landmarks(img_bgr, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    return img_bgr, len(hands)


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

                img, _ = annotate_frame(hand_detector, img)
                cv2.imshow("Hand Tracking", img)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
