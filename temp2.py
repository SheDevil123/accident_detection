from ultralytics import YOLO
from PIL import Image
import cv2

model = YOLO("yolov8x.pt")

"""https://docs.ultralytics.com/reference/yolo/engine/results/#ultralytics.yolo.engine.results.Boxes"""
cap=cv2.VideoCapture(0)
#r"E:\yolov5\bike and ped.mp4"
while True:
    _,frame=cap.read()
    results = model.track(source=frame,show=False,persist=True) 
    if results[0].boxes.id != None:
        ids=results[0].boxes.id.numpy().astype(int)
        confs=results[0].boxes.conf.numpy().astype(float)
        clss=results[0].boxes.cls.numpy().astype(int)
        boxes=results[0].boxes.xyxy.numpy().astype(int)
    img=results[0].plot()
    cv2.imshow("",img)
    for j,i in enumerate(clss):
        if i==0:
            print((boxes[j][2]-boxes[j][0])/(boxes[j][3]-boxes[j][1]))

    if cv2.waitKey(20)==ord('q'):
        break