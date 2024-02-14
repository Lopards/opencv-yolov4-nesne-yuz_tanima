import cv2


net = cv2.dnn.readNet("dnn_model/yolov4-tiny.weights", "dnn_model/yolov4-tiny.cfg")
model = cv2.dnn.DetectionModel(net)
model.setInputParams(size=(320, 320),scale=1/255)
# DNN modelini yükleyip, giriş parametrelerini belirledik.


# classes.txt dosyasındaki sınıf isimlerini alıp, 'classes' listesine ekledik.
classes = []
with open("dnn_model/classes.txt","r") as file_object:
    for line in file_object:
        line = line.strip() # Satır sonundaki boşlukları temizledik.
        classes.append(line)

#Burada x ve y ekranda tıklanan yern koordinatlarıdır
def click_button(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:# eğer event yani bir tıklanma varsa sol klik
        print(x,y)


#pencerede mousa tıkladığımızda click_button isimli metod çağırılıyor
cv2.namedWindow("frame")
cv2.setMouseCallback("frame",click_button)

cap = cv2.VideoCapture(0)#kamerayı seçtik
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
#kamera görüntü çercevesini büyüttük


while True:
    ret, frame = cap.read()
    # Kameradan bir kare okuyup, nesneleri tespit etmeye çalışıyoruz.
    (class_ids, scores, boxes) = model.detect(frame, confThreshold=0.3, nmsThreshold=0.4)
    for class_id, score, box in zip(class_ids, scores, boxes):
        (x, y, w, h) = box
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)
        # Nesne tespit edildiğinde dikdörtgen çiziyoruz.

        class_name = classes[class_id]
        cv2.putText(frame, class_name, (x, y-10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0))
        # Tespit edilen nesnenin adını ekrana yazıyoruz.

        cv2.rectangle(frame, (20, 20), (220,70),(0,0,220),-1) #kutucuk oluşturuyoruz sırasıyal koordinat, genişliği rengi ve -1 ise içinin renge boyanması
        cv2.putText(frame,"person",(30,60),cv2.FONT_HERSHEY_PLAIN, 2,(255,255,255),3)

    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
# Kamera kaynağını serbest bırakıp, pencereyi kapatıyoruz.
