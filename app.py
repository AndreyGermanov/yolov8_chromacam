import os
import cv2
import time
from threading import Thread
from flask import Flask, request
from waitress import serve
import os.path as path
from ultralytics import YOLO
import numpy as np

app = Flask(__name__, static_url_path='', static_folder='.')

# Default blur value
blur = 0

def main():

    # Run camera processing in separate thread
    thread = Thread(target=run_camera)
    thread.start()

    print("Web server starting on port 8080")

    # Run web service in a main thread
    serve(app, port=8080)


@app.route('/')
def root():
    """
    Handler of default route
    """
    return app.send_static_file('index.html')


@app.route('/background', methods=["POST"])
def set_background():
    """
    Function receives uploaded image file
    and writes it as a current background
    for frames
    """
    file = request.files.get("background")
    if file is not None:
        file.save(file.filename)
        img = cv2.imread(file.filename)
        cv2.imwrite("bg.jpg", img)
        os.remove(file.filename)
        return "OK"


@app.route('/blur/<blur_value>')
def change_blur(blur_value):
    """
    Sets blur value from GET request
    """
    global blur
    blur = int(blur_value)
    return "OK"


@app.route("/reset")
def reset():
    """
    Function resets blur and background    
    """
    global blur
    if path.isfile("bg.jpg"):
        os.remove("bg.jpg")
    blur = 0
    x = 0
    y = 0
    return "OK"


def run_camera():
    """
    Function captures each video frame from web camera
    as OpenCV image in a background thread,
    detects person on each frame,
    replaces and blurs background around this person
    """

    # Connect to the default web camera
    source = cv2.VideoCapture(0)

    # capture frames from web camera every 30 ms
    while True:
        has_frame, frame = source.read()

        if not has_frame:
            break

        # pass the frame through YOLOv8 model and return
        # a segmentation mask of a person
        mask = get_person_mask(frame)

        # change background and/or apply blur
        frame = apply_background_options(frame, mask)

        cv2.imwrite("temp.jpg", frame)
        os.rename("temp.jpg", "frame.jpg")
        time.sleep(0.03)


def get_person_mask(frame):
    """
    Function attempts to detect
    segmentation mask of a person
    on current video frame
    and returns it
    """

    model = YOLO("yolov8m-seg.pt")
    results = model.predict(frame, verbose=False)
    if results is None or len(results) == 0:
        return

    result = results[0]

    # get all detected persons on the frame
    classes = [index for (index, cls) in enumerate(result.boxes.cls.numpy()) if cls == 0]
    if len(classes) == 0:
        return

    # get segmentation mask of the first detected person
    index = classes[0]
    mask = result.masks.data[index].numpy().astype('uint8')
    # resize to the size of frame, if needed
    mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))

    return mask


def apply_background_options(frame, mask):
    """
    Function applies new background and
    blur for all pixels of specified
    frame except the pixels, that included
    in the person mask 
    """

    # If background uploaded, use it
    # otherwise, treat the frame itself as a background
    if path.isfile("bg.jpg"):
        bg = cv2.imread("bg.jpg")
        bg = cv2.resize(bg, (frame.shape[1], frame.shape[0]))
    else:
        bg = frame[:, :, :]

    # apply blur to background if specified
    if blur > 0:
        bg = set_blur(bg, blur)    

    # change all pixels of the frame
    # except pixels included to the person mask
    # to pixels from background
    if mask is not None:
        frame[mask == 0] = bg[mask == 0]
    else:
        frame = bg
    return frame


def set_blur(frame, value):
    """
    Function applies blur to specified frame
    """
    if value == 0:
        return frame
    return cv2.blur(frame, (value, value))


main()
