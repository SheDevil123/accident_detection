from ultralytics import YOLO
from PIL import Image
import cv2

model = YOLO("yolov8x.pt")

def mid(boxes):
    return ((boxes[0]+boxes[2])//2,(boxes[1]+boxes[3])//2)

def dist(p1,p2):
    return (((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))**0.5
"""https://docs.ultralytics.com/reference/yolo/engine/results/#ultralytics.yolo.engine.results.Boxes"""
cap=cv2.VideoCapture(r"E:\yolov5\weird clip.mp4")

notify=[]
bike=[]
person=[]
person_down={}

save=True
if save:
    fps=cap.get(cv2.CAP_PROP_FPS)
    save_file = cv2.VideoWriter('bike ped coollision and person on floor.mp4', cv2.VideoWriter_fourcc(*'mp4v'),fps, (int(cap.get(3)),int(cap.get(4))))

while True:
    res,frame=cap.read()
    #print(frame.shape)
    if not res:
        break
    img=frame
    #print(frame.shape)
    img=frame
    results = model.track(source=frame,show=False,persist=True) 
    #print(type(results))
    #print(type(results[0]))
    if results[0].boxes.id != None:
        ids=results[0].boxes.id.numpy().astype(int)
        confs=results[0].boxes.conf.numpy().astype(float)
        clss=results[0].boxes.cls.numpy().astype(int)
        boxes=results[0].boxes.xyxy.numpy().astype(int)

    #registring bike locations
    for j,i in enumerate(clss):
        if i==3:
            bike.append([boxes[j],50,ids[j]])
        if i==0 and (boxes[j][2]-boxes[j][0])/(boxes[j][3]-boxes[j][1])>1:
            if ids[j] not in person:
                person.append(ids[j])
                person_down[ids[j]]=[[boxes[j],15]]
            elif ids[j] in person_down.keys():
                #print(person_down(ids[j]))
                print(person_down)
                if len(person_down[ids[j]])>10:
                    person_down[ids[j]].pop(0)
                person_down[ids[j]].append([boxes[j],15])

    #removing old bikes
    #print(bike)
    temp=[]
    for i in range(len(bike)):
        bike[i][1]-=1
        if bike[i][1]<0:
            temp.append(i)
    
    bike=[bike[i] for i in range(len(bike)) if i not in temp]
    
    temp=[]
    for i in person_down.keys():
        person_down[i][-1][-1]-=1
        if person_down[i][-1][-1]<0:
            temp.append(i)
        loc=mid(person_down[i][-1][0])
        for j in bike:
            print(loc,mid(j[0]))
            if dist(loc,mid(j[0]))<30:
                img=cv2.rectangle(img,j[0][:2],j[0][2:],(0,0,255),3)
                img=cv2.putText(img,"possible crash",(j[0][0],j[0][1]-10),cv2.FONT_HERSHEY_TRIPLEX,1,(0,0,0),2,cv2.LINE_AA)
                img=cv2.putText(img,"possible crash",(150,150),cv2.FONT_HERSHEY_TRIPLEX,2,(0,0,255),2,cv2.LINE_AA)
                break

        print(person_down[i])
        img=cv2.rectangle(img,person_down[i][-1][0][:2],person_down[i][-1][0][2:],(255,0,0),2)
        img=cv2.putText(img,"Pedestrian lying on the road",(person_down[i][-1][0][0],person_down[i][-1][0][1]+10),cv2.FONT_HERSHEY_TRIPLEX,1,(0,0,0),2,cv2.LINE_AA)
    
    person_down={key:val for key,val in person_down.items() if key not in temp }
        


    #img=results[0].plot()
    cv2.imshow("",img)
    if save:
        save_file.write(img)

    if cv2.waitKey(20)==ord('q'):
        break

cap.release()
save_file.release()