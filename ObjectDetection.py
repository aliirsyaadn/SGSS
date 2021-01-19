import cv2
from datetime import datetime
# Change directory path to your absolute path
classNames= []
classFile = '/home/pi/Documents/embedded/SGSS/objectDetectionData/coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath = '/home/pi/Documents/embedded/SGSS/objectDetectionData/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = '/home/pi/Documents/embedded/SGSS/objectDetectionData/frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nms)
    
    if len(objects) == 0: objects = classNames
    objectInfo = []
    detected = False
    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects:
                detected = True
                objectInfo.append([box, className])
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                                cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                                cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        
    return img, objectInfo, detected

def capturePhoto():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    success,img = cap.read()
    img = cv2.rotate(img, cv2.ROTATE_180)
    result, objectInfo, detected = getObjects(img, 0.60, 0.2, objects=['person'])
   
    name = datetime.now().strftime("%m%d%Y%H%M%S")
    cv2.waitKey(1)
    cv2.imwrite(f'./output/{name}.jpg',result)
    
    cap.release()

    return detected

if __name__ == "__main__":
    capturePhoto()