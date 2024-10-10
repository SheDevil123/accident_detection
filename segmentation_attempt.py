from ultralytics import YOLO
import cv2

model=YOLO("yolov8x-seg.pt")

cap=cv2.VideoCapture(0)
while True:
    _,frame=cap.read()
    results=model.predict(source=frame,show=True)
    print(type(results[0].masks))
    break
    

    if cv2.waitKey(20)==ord('q'):
        break
