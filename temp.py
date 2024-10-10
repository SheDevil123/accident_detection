from ultralytics import YOLO
from PIL import Image
import cv2

model = YOLO(r"E:\yolov5\best.pt")
# accepts all formats - image/dir/Path/URL/video/PIL/ndarray. 0 for webcam
#results = model.predict(source="0", show=True,classes=[67],retina_masks=True) 

# Display preds. Accepts all YOLO predict arguments


cap=cv2.VideoCapture(0)
#results = model.track(source="0",show=True) 

while True:
    _,frame=cap.read()
    # results = model.track(source=frame,show=True) 
    results = model.predict(source=frame,show=True)
    img=results[0].plot()
    cv2.imshow("",img)
    # print(results[0].boxes)  
    # print(results[0])  
    if cv2.waitKey(20)==ord('q'):
        break
     # save plotted images
# for result in results:
#     print(result.boxes)  # Boxes object for bbox outputs
#     print(result.masks)  # Masks object for segmenation masks outputs
#     print(result.probs)  # Class probabilities for classification outputs

# # from ndarray
# im2 = cv2.imread("bus.jpg")
# results = model.predict(source=im2, save=True, save_txt=True)  # save predictions as labels

# from list of PIL/ndarray
#results = model.predict(source=[im1, im2])