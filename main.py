import cv2
from datetime import datetime
import os
import time

# --------------------------------
# CREATE FOLDERS
# --------------------------------
os.makedirs("captures", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# --------------------------------
# TIMER TO PREVENT SPAM SAVING
# --------------------------------
last_saved_time = 0

# --------------------------------
# OPEN WEBCAM
# --------------------------------
cap = cv2.VideoCapture(0)

# --------------------------------
# MAIN LOOP
# --------------------------------
while True:

    success, frame = cap.read()

    if not success:
        print("Camera not working")
        break

    # --------------------------------
    # DISPLAY STATUS TEXT
    # --------------------------------
    cv2.putText(
        frame,
        "AI SECURITY ACTIVE",
        (50, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # --------------------------------
    # SHOW CAMERA
    # --------------------------------
    cv2.imshow("AI Security System", frame)

    # --------------------------------
    # KEYBOARD INPUT
    # --------------------------------
    key = cv2.waitKey(1)

    # --------------------------------
    # CURRENT TIME
    # --------------------------------
    current_time = time.time()

    # --------------------------------
    # PRESS 'S' TO SAVE DETECTION
    # --------------------------------
    if key == ord('s'):

        # SAVE ONLY EVERY 5 SECONDS
        if current_time - last_saved_time > 5:

            # TIMESTAMP
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            # IMAGE PATH
            image_path = f"captures/{timestamp}.jpg"

            # SAVE IMAGE
            cv2.imwrite(image_path, frame)

            # LOG MESSAGE
            log_message = f"[{timestamp}] Human detected -> {image_path}\n"

            # SAVE LOG
            with open("logs/detection_log.txt", "a") as file:
                file.write(log_message)

            print("Detection Saved!")
            print(log_message)

            # UPDATE LAST SAVED TIME
            last_saved_time = current_time

        else:
            print("Wait 5 seconds before saving again...")

    # --------------------------------
    # PRESS 'Q' TO QUIT
    # --------------------------------
    if key == ord('q'):
        break

# --------------------------------
# RELEASE CAMERA
# --------------------------------
cap.release()
cv2.destroyAllWindows()
