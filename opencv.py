import cv2

net = cv2.dnn.readNet("dnn_model/yolov4-tiny.weights", "dnn_model/yolov4-tiny.cfg")
model = cv2.dnn.DetectionModel(net)
model.setInputParams(size=(320, 320),scale=1/255)
#burada dnn modelini tanımladık


cap = cv2.VideoCapture(0) # kamerayı belirle

while True:
    ret, frame = cap.read()
    #burada nesneyi tanımaya çalışacağız
    (class_ids,scores,boxes) = model.detect(frame, confThreshold=0.5, nmsThreshold=.4)
    #burda değerlerle oynayarak tanıma hızını değiştirebiliriz ancak değeri ne kadar azaltırsak sapıtma durumu o kadar artar 
  
    for class_ids,score,box in zip(class_ids,scores,boxes): # 3 tane for döngüsü yapmak yerine zip komutu ile yapıyoruz
        (x,y,w,h) = box
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3) # burada nesne tanımlandığında dikdörtgen çiziliyor
        cv2.putText(frame,str(class_ids),(x,y-10),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0))
    cv2.imshow('frame',frame)
    key = cv2.waitKey(1)
    if key == 27: #ESC tuşuna basıldığında sonlandır
      break


cap.release()
cv2.destroyAllWindows()
