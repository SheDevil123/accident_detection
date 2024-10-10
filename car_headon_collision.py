from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np

def dist(p1,p2):
    return (((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))**0.5

save=True
ref=(0,720)
model = YOLO("yolov5x.pt")
timer=0
crash=[]
wrong_way=[]
correct_way=[]

"""https://docs.ultralytics.com/reference/yolo/engine/results/#ultralytics.yolo.engine.results.Boxes"""
cap=cv2.VideoCapture(r"E:\yolov5\car_clip2.mp4")
# for _ in range(50):
#     cap.read()
data={}
if save:
    fps=cap.get(cv2.CAP_PROP_FPS)
    save_file = cv2.VideoWriter('save_headon_collison_testing.mp4', cv2.VideoWriter_fourcc(*'mp4v'),fps, (int(cap.get(3)),int(cap.get(4))))
while True:
    is_frame,frame=cap.read()
    if not is_frame:
        break
    #print(frame.shape)
    img=frame
    results = model.track(source=frame,show=False,persist=True) 
    #print(type(results))
    #print(type(results[0]))
    ids=results[0].boxes.id.numpy().astype(int)
    # print(ids.numpy())
    confs=results[0].boxes.conf.numpy().astype(float)
    clss=results[0].boxes.cls.numpy().astype(int)
    boxes=results[0].boxes.xyxy.numpy().astype(int)
    # print(results[0].boxes.xyxy)

    #adding stuff to data
    for j,i in enumerate(clss):
        if i==2:
            if f"{ids[j]}" in data.keys() and len(data[f"{ids[j]}"])>=24:
                data[f"{ids[j]}"].pop(0)
            pos=((boxes[j][0]+boxes[j][2])//2,(boxes[j][1]+boxes[j][3])//2)
            if f"{ids[j]}" not in data.keys():
                data[f"{ids[j]}"]=[]
            data[f"{ids[j]}"].append([pos,boxes[j].astype(int),confs[j],0])
    temp=[]
    #deleting old records
    for j,i in enumerate(data.keys()):
        if int(i) not in ids:
            data[i][-1][2]+=1
            if data[i][-1][2]>=24:
                temp.append(i)
        else:
            data[i][-1][2]=0    

    #deletion
    data= { key:val for key, val in data.items() if key not in temp }
    #print(data)
    for i in data.keys():
        if len(data[i])>5:
            #print(dist(ref,data[i][-1][0]) , dist(ref,data[i][-4][0]))
            if dist(ref,data[i][-1][0]) < dist(ref,data[i][-2][0]):
                img=cv2.rectangle(img,data[i][-1][1][:2],data[i][-1][1][2:],(0,0,255),2)
                img=cv2.putText(img,"wrong_way",(data[i][-1][1][0],data[i][-1][1][1]+10),cv2.FONT_HERSHEY_TRIPLEX,1,(0,0,255),1,cv2.LINE_AA)
                if i not in correct_way and not i in wrong_way:
                    wrong_way.append(i)
            else:
                img=cv2.rectangle(img,data[i][-1][1][:2],data[i][-1][1][2:],(0,255,0),2)
                img=cv2.putText(img,"correct_way",(data[i][-1][1][0],data[i][-1][1][1]+10),cv2.FONT_HERSHEY_TRIPLEX,1,(0,255,0),1,cv2.LINE_AA)
                if i not in wrong_way and i not in correct_way:
                    correct_way.append(i)
    img=results[0].plot()
    print(wrong_way,correct_way)
    if timer<=0:
        for i in wrong_way:
            for j in correct_way:
                #print(data[i][-1][1],data[j][-1][1])
                print(abs(dist(data[j][0][0][:2],data[i][0][0][:2]) - dist(data[j][-1][0][:2],data[i][-1][0][:2])),i,j)
                if abs(dist(data[j][0][0][:2],data[i][0][0][:2]) - dist(data[j][-1][0][:2],data[i][-1][0][:2])) <=5:
                    print(i,j)
                    crash.append([[min(data[i][-1][1][0],data[j][-1][1][0]),min(data[i][-1][1][1],data[j][-1][1][1])],[max(data[i][-1][1][2],data[j][-1][1][2]),max(data[i][-1][1][3],data[j][-1][1][3])]])
                    timer=1000
    timer-=1
    print(crash)
    if crash:
        img=cv2.rectangle(img,crash[0][0],crash[0][1],(0,0,255),5)
        img=cv2.putText(img,"crash",(crash[0][0][0],crash[0][0][1]+10),cv2.FONT_HERSHEY_TRIPLEX,1,(0,255,0),2,cv2.LINE_AA)
    cv2.imshow("",img)

    if save:
        save_file.write(img)
    #cv2.waitKey(0)
    if cv2.waitKey(20)==ord('q'):
        break


save_file.release()
cap.release()
