import cv2
import time
import os

def run_motion_detection():
    cap = cv2.VideoCapture(0)

    os.makedirs("captures", exist_ok=True)

    # 🔥 Human detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    last_event_time = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Resize for speed
        frame = cv2.resize(frame, (640, 480))

        # Detect humans
        boxes, _ = hog.detectMultiScale(frame, winStride=(8,8))

        for (x, y, w, h) in boxes:
            
            # ⏱️ Cooldown
            if time.time() - last_event_time > 5:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                filename = f"captures/human_{timestamp.replace(':','-')}.jpg"

                cv2.imwrite(filename, frame)

                with open("log.txt", "a") as f:
                    f.write(f"Human detected at {timestamp}\n")

                os.system("say Human detected")

                print(f"[+] Human detected at {timestamp}")

                last_event_time = time.time()

            # Draw box
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)

        cv2.imshow("AI Human Detection", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
