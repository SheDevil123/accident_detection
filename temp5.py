from ultralytics import YOLO
import numpy as np

model=YOLO("E:\yolov5\(Game)best.pt")
result=model.predict(source="real.jpg",show=True,save=True)
# for i in result[0].boxes.cls.cpu().numpy():
#     print(i)
# print(result[0].names)
# printf(result)