# Chroma Cam effect using YOLOv8 neural network.


This web application shows how to replace or blur background around person on a web camera using YOLOv8 neural network
and without green screen.

See demo video: https://youtu.be/pOQBbrPBfW4

It's based on the app from this repository: https://github.com/AndreyGermanov/opencv_webcam_filtering_webapp.

This is an addition to the article "[How to implement instance segmentation using YOLOv8 neural network](https://dev.to/andreygermanov/how-to-implement-instance-segmentation-using-yolov8-neural-network-3if9)". 

Read it to understand the code.
## Install

* Clone this repository: `git clone git@github.com:AndreyGermanov/opencv_webcam_filtering_webapp`
* Go to the root of cloned repository
* Install dependencies by running `pip3 install -r requirements.txt`

## Run

Ensure that web camera connected and not busy by other applications.

Execute:

```
python3 app.py
```

It will start a webserver on http://localhost:8080. Use any web browser to open the web interface.

Using the interface you can play with video from web camera by change or blur background.

It's recommended to run this on computers with GPU, to avoid delays in video processing.