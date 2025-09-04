import cv2
import mediapipe as mp

def get_gesture_name(landmarks, handedness):
    finger_tips = [4, 8, 12, 16, 20]
    finger_is_open = []
    
    is_left_hand = handedness.classification[0].label == 'Left'
    
    # Thumb check
    thumb_tip_y = landmarks.landmark[finger_tips[0]].y
    thumb_cmc_y = landmarks.landmark[1].y
    
    if is_left_hand:
        if landmarks.landmark[4].x < landmarks.landmark[3].x:
            finger_is_open.append(True)
        else:
            finger_is_open.append(False)
    else: # Right Hand
        if landmarks.landmark[4].x > landmarks.landmark[3].x:
            finger_is_open.append(True)
        else:
            finger_is_open.append(False)

    # Other four fingers check (Index, Middle, Ring, Pinky)
    for i in range(1, 5):
        tip_y = landmarks.landmark[finger_tips[i]].y
        pip_y = landmarks.landmark[finger_tips[i] - 2].y
        
        if tip_y < pip_y:
            finger_is_open.append(True)
        else:
            finger_is_open.append(False)
    
    # Gesture Classification - Ordered from most specific to least specific
    if all(finger_is_open):
        return "Open Palm"
    elif not any(finger_is_open):
        return "Fist"
    elif finger_is_open == [False, True, True, False, False]:
        return "Peace Sign"
    elif finger_is_open == [True, False, False, False, False]:
        if landmarks.landmark[4].y > landmarks.landmark[3].y:
            return "Thumbs Down"
        else:
            return "Thumbs Up"
    elif finger_is_open == [False, True, False, False, False]:
        return "Point Up"
    elif finger_is_open == [True, False, False, False, True]:
        return "I Love You"
    elif finger_is_open == [False, True, True, False, True]:
        return "Spock"
    elif finger_is_open == [False, False, False, False, True]:
        return "Pinky Up"
    elif finger_is_open == [False, True, True, True, True]:
        return "Four Fingers Up"
    elif finger_is_open == [False, False, True, True, True]:
        return "Three Fingers Up"
    elif finger_is_open == [True, True, False, False, False]:
        return "L Sign"
    elif finger_is_open == [True, True, False, False, True]:
        return "Rock On"
    else:
        return "Unknown"

def main():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
    mp_draw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        success, image = cap.read()
        if not success:
            continue

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        gesture_name = "No Hand Detected"

        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                gesture_name = get_gesture_name(hand_landmarks, handedness)
                mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                h, w, _ = image.shape
                x_max, y_max = 0, 0
                x_min, y_min = w, h
                
                for lm in hand_landmarks.landmark:
                    x, y = int(lm.x * w), int(lm.y * h)
                    x_max = max(x_max, x)
                    x_min = min(x_min, x)
                    y_max = max(y_max, y)
                    y_min = min(y_min, y)
                cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

        cv2.putText(image, gesture_name, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Hand Gesture Recognition', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()