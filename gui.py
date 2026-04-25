import cv2
import time
import os
import tkinter as tk
from PIL import Image, ImageTk
from ultralytics import YOLO

# Load YOLO model (downloads automatically first time)
model = YOLO("yolov8n.pt")

class SecurityApp:
    def __init__(self, window):
        self.window = window
        self.window.title("AI Security System")

        self.cap = None
        self.running = False
        self.last_event_time = 0

        # Create folder
        os.makedirs("captures", exist_ok=True)

        # Canvas
        self.canvas = tk.Canvas(window, width=640, height=480)
        self.canvas.pack()

        # Buttons
        self.btn_start = tk.Button(window, text="Start Camera", command=self.start)
        self.btn_start.pack()

        self.btn_stop = tk.Button(window, text="Stop Camera", command=self.stop)
        self.btn_stop.pack()

    def start(self):
        self.cap = cv2.VideoCapture(0)
        self.running = True
        self.update()

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()

    def update(self):
        if self.running:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, (640, 480))

                # 🔥 YOLO detection
                results = model(frame)

                for r in results:
                    for box in r.boxes:
                        cls = int(box.cls[0])

                        if cls == 0:  # person
                            x1, y1, x2, y2 = map(int, box.xyxy[0])

                            # ⏱️ Cooldown
                            if time.time() - self.last_event_time > 5:
                                timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
                                filename = f"captures/person_{timestamp}.jpg"

                                # 📸 Save image
                                cv2.imwrite(filename, frame)

                                # 📝 Log
                                with open("log.txt", "a") as f:
                                    f.write(f"Person detected at {timestamp}\n")

                                # 🔔 Voice alert
                                os.system("say Person detected")

                                print(f"[+] Person detected at {timestamp}")

                                self.last_event_time = time.time()

                            # Draw box
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Convert for Tkinter
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)

                self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
                self.canvas.imgtk = imgtk

            self.window.after(10, self.update)

# Run app
root = tk.Tk()
app = SecurityApp(root)
root.mainloop()
