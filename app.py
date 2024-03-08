from flask import Flask, render_template, send_from_directory
from ultralytics import YOLO
import cv2
import math
import pygame
import threading
import time
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime

app = Flask(__name__)

# Initialize pygame for playing alarm sound
pygame.init()

# Load the alarm sound
path_alarm = r"alarm.wav"
alarm_sound = pygame.mixer.Sound(path_alarm)

# Load YOLO model
model = YOLO("yolo-Weights/yolov8n.pt")

# Object classes
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "LETHAL WEAPON",
              "teddy bear", "hair drier", "toothbrush"
              ]

# Capture video from the webcam
cap = cv2.VideoCapture(0)

# Initialize variables for controlling detection
stop_detection = False
pause_detection = False
alarm_playing = False
flask_started = False
screenshot_limit = 10
screenshot_count = 0

# List to store paths of detected images
detected_image_paths = []


def yolo_detection():
    global stop_detection, pause_detection, alarm_playing, flask_started, screenshot_count

    # Path to the directory containing the captured images
    image_directory = "images"

    # Create the directory if it does not exist
    os.makedirs(image_directory, exist_ok=True)

    last_person_img = None
    person_counter = 0
    while True:
        if stop_detection:
            break

        # Check for key press
        key = cv2.waitKey(1)
        if key == ord('q'):
            stop_detection = True
            if alarm_playing:
                alarm_sound.stop()
                alarm_playing = False
            if not flask_started:
                start_flask()  # Start Flask app if not already started
            break
        elif key == ord('p'):
            pause_detection = not pause_detection

        if not pause_detection:
            success, img = cap.read()
            img = cv2.resize(img, (1280, 720))
            results = model(img, stream=True)
            person_detected = False
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    confidence = math.ceil((box.conf[0] * 100)) / 100
                    cls = int(box.cls[0])
                    class_name = classNames[cls]
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    org = (x1, y1)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 1
                    color = (255, 0, 0)
                    thickness = 2
                    cv2.putText(img, class_name, org, font, fontScale, color, thickness)
                    if class_name == "person":
                        person_detected = True
                        person_counter += 1
                        last_person_img = img.copy()
                        cv2.imwrite(os.path.join(image_directory, f"person_{person_counter}.jpg"), last_person_img)
                        detected_image_paths.append(os.path.join(image_directory, f"person_{person_counter}.jpg"))
                        time.sleep(0.8)
                        screenshot_count += 1
                        if screenshot_count >= screenshot_limit:
                            stop_detection = True
                            break
            if person_detected and not alarm_playing:
                alarm_sound.play()
                alarm_playing = True
            elif not person_detected and alarm_playing:
                alarm_sound.stop()
                alarm_playing = False
            cv2.imshow('Webcam', img)

    cap.release()
    cv2.destroyAllWindows()


def send_email_notification():
    sender_email = "gecbhsender@gmail.com"
    receiver_email = "gecbhsender@gmail.com"
    password = "zamsewsuqdkzgtze"
#["gecbhsender@gmail.com", "akshayspasp@gmail.com", "jayasuryajs2002911@gmail.com", "adershsthomas@gmail.com","vijayanand.ks@gecbh.ac.in","ksvijayanand@gmail.com"]
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_email)
    msg['Subject'] = "Intruder Detected @ " + time.strftime("%Y-%m-%d %H:%M:%S")

    html =   """
<html>
      <head>
      </head>
      <body style="background-color: #000000; color: #ffffff; font-family: Arial, sans-serif;">
        <h1 style="color: #00ff00;">Intruder Detected</h1>
        <p>A person has been detected.</p>
        <p>{timestamp}</p>
        <p>Please see the attached images.</p>
      </body>
    </html>
""".format(timestamp=time.strftime("%Y-%m-%d %H:%M:%S"))

    msg.attach(MIMEText(html, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)

    for image_path in detected_image_paths:
        with open(image_path, 'rb') as attachment:
            image_part = MIMEImage(attachment.read(), _subtype="jpg")
            image_part.add_header('Content-Disposition', "attachment; filename= %s" % os.path.basename(image_path))
            msg.attach(image_part)

    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()


@app.route('/')
def index():
    # Get all image paths with their filenames and timestamps
    image_data = [
        {
            "path": os.path.join("images", f),
            "filename": f,
            "timestamp": datetime.fromtimestamp(os.path.getmtime(os.path.join("images", f))).strftime(
                '%Y-%m-%d %H:%M:%S')
        }
        for f in os.listdir("images") if f.startswith("person_")
    ]

    # Limit the number of images to the first 10
    image_data = image_data[:10]

    return render_template('index.html', image_data=image_data)


# Route to serve the last person's image
@app.route('/image/<path:filename>')
def get_image(filename):
    return send_from_directory("images", filename)


def start_flask():
    global flask_started
    flask_started = True
    app.run(debug=True, use_reloader=False)  # Disable the reloader


if __name__ == '__main__':
    # Start YOLO object detection in a separate thread
    yolo_thread = threading.Thread(target=yolo_detection)
    yolo_thread.start()

    # Wait for YOLO detection to complete
    yolo_thread.join()

    # Send email notification after all pictures are taken
    send_email_notification()

    # Start Flask app after YOLO detection and email notification
    start_flask()
