from ultralytics import YOLO
from PIL import Image
import cv2

model = YOLO("yolov8x.pt")

"""https://docs.ultralytics.com/reference/yolo/engine/results/#ultralytics.yolo.engine.results.Boxes"""
cap=cv2.VideoCapture(r"E:\yolov5\weird clip.mp4")
while True:
    _,frame=cap.read()
    results = model.track(source=frame,show=False,persist=True) 
    print(type(results))
    print(type(results[0]))
    ids=results[0].boxes.id
    print(ids)
    print(results[0].boxes.conf)
    img=results[0].plot()
    cv2.imshow("",img)

    if cv2.waitKey(20)==ord('q'):
        break