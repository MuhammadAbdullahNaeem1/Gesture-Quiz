
import random


def generate_equation():

    operators = ['+', '-', '*', '/']
    op = random.choice(operators)

    if op == '+':
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        return f"{a} + ? = {a+b}", b
    elif op == '-':
        a = random.randint(1, 9)
        b = random.randint(0, a)
        return f"{a} - ? = {a-b}", b
    elif op == '*':
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        return f"{a} * ? = {a*b}", b
    elif op == '/':
        b = random.randint(1, 9)
        a = b * random.randint(1, 9)
        return f"{a} / ? = {a//b}", b



def hand_gesture_math_game_with_timer_v4():
    import cv2
    import mediapipe as mp
    import time

    cap = cv2.VideoCapture(0)

    medhands = mp.solutions.hands
    hands = medhands.Hands(max_num_hands=2, min_detection_confidence=0.7)
    draw = mp.solutions.drawing_utils

    score = 0
    question_count = 0
    equation, answer = generate_equation()
    feedback = ""
    feedback_display_time = 0
    countdown_duration = 10
    countdown = countdown_duration
    start_time = time.time()

    while question_count < 10:
        success, img = cap.read()
        h, w, c = img.shape
        img = cv2.flip(img, 1)
        imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = hands.process(imgrgb)

        total_fingers_shown = 0
        tipids = [4, 8, 12, 16, 20]  # landmarks of the tips of fingers

        if res.multi_hand_landmarks:
            for handlms in res.multi_hand_landmarks:
                lmlist = []
                for id, lm in enumerate(handlms.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmlist.append([id, cx, cy])

                if len(lmlist) != 0 and len(lmlist) == 21:
                    fingerlist = []

                    # Thumb, considering flipping of hands
                    if lmlist[12][1] > lmlist[20][1]:
                        if lmlist[tipids[0]][1] > lmlist[tipids[0] - 1][1]:
                            fingerlist.append(1)
                        else:
                            fingerlist.append(0)
                    else:
                        if lmlist[tipids[0]][1] < lmlist[tipids[0] - 1][1]:
                            fingerlist.append(1)
                        else:
                            fingerlist.append(0)

                    # Other fingers
                    for id in range(1, 5):
                        if lmlist[tipids[id]][2] < lmlist[tipids[id] - 2][2]:
                            fingerlist.append(1)
                        else:
                            fingerlist.append(0)

                    if len(fingerlist) != 0:
                        total_fingers_shown += fingerlist.count(1)

                # Draw hand landmarks
                draw.draw_landmarks(img, handlms, medhands.HAND_CONNECTIONS,
                                    draw.DrawingSpec(
                                        color=(0, 255, 204), thickness=2, circle_radius=2),
                                    draw.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=3))

        # Check if the countdown is over
        elapsed_time = time.time() - start_time
        if elapsed_time > countdown_duration:
            if total_fingers_shown == answer:
                feedback = "Correct"
                score += 1
            else:
                feedback = "Incorrect"

            feedback_display_time = time.time()
            # Reset for next question
            start_time = time.time()
            equation, answer = generate_equation()
            question_count += 1
        else:
            countdown = countdown_duration - int(elapsed_time)

            # Show the feedback for 3 seconds
            if feedback and time.time() - feedback_display_time > 3:
                feedback = ""

        cv2.putText(img, feedback, (100, 200),
                    cv2.FONT_HERSHEY_TRIPLEX, 3, (0, 255, 0), 5)
        cv2.putText(img, equation, (50, 50),
                    cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 0, 0), 3)
        cv2.putText(img, f"Detected: {total_fingers_shown}", (w -
                    250, h - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(img, f"Score: {score}", (w - 200, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(img, f"Countdown: {countdown}", (50, h - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Math Game with Countdown", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Display final score after 10 questions
    while True:
        img[:] = 0  # black background
        cv2.putText(img, "Congratulations Abdullah", (w//8, h//3),
                    cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 0), 4)
        cv2.putText(img, f"Your score is:", (w//8, h//2),
                    cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 0), 4)
        cv2.putText(img, f"{score}/10", (w//8, 2*h//3),
                    cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 0), 4)
        cv2.imshow("Math Game with Countdown", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# The actual webcam feed and hand gesture detection will work only when this code is run on a local machine with a camera
hand_gesture_math_game_with_timer_v4()
