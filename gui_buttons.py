#opencv.py dosyasındaki butonları gösteren ve ekleten py dosyası
import cv2
import numpy as np

class Butonlar:
    def __init__(self):
        # Yazı tipi
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.text_olcegi = 3
        self.text_kalinlik = 3
        self.x_marg = 20
        self.y_marg = 10

        # Düğmeler
        self.dugmeler = {}
        self.dugme_index = 0
        self.dugmeler_alani = []

        np.random.seed(0)
        self.renkler = []
        self.rastgele_renkler_olustur()

    def rastgele_renkler_olustur(self):
        for i in range(91):
            rastgele_renk = np.random.randint(256, size=3)
            self.renkler.append((int(rastgele_renk[0]), int(rastgele_renk[1]), int(rastgele_renk[2])))

    def buton_ekle(self, metin, x, y):
        # Metin boyutunu al
        metin_boyutu = cv2.getTextSize(metin, self.font, self.text_olcegi, self.text_kalinlik)[0]
        sag_x = x + (self.x_marg * 2) + metin_boyutu[0]
        alt_y = y + (self.y_marg * 2) + metin_boyutu[1]

        self.dugmeler[self.dugme_index] = {"metin": metin, "pozisyon": [x, y, sag_x, alt_y], "aktif": False}
        self.dugme_index += 1

    def buton_goster(self, cerceve):
        for d_index, dugme_degeri in self.dugmeler.items():
            dugme_metni = dugme_degeri["metin"]
            (x, y, sag_x, alt_y) = dugme_degeri["pozisyon"]
            aktif = dugme_degeri["aktif"]

            if aktif:
                dugme_rengi = (0, 0, 200)
                metin_rengi = (255, 255, 255)
                kalinlik = -1
            else:
                dugme_rengi = (0, 0, 200)
                metin_rengi = (0, 0, 200)
                kalinlik = 3

            # Metin boyutunu al
            cv2.rectangle(cerceve, (x, y), (sag_x, alt_y), dugme_rengi, kalinlik)
            cv2.putText(cerceve, dugme_metni, (x + self.x_marg, alt_y - self.y_marg),
                        self.font, self.text_olcegi, metin_rengi, self.text_kalinlik)
        return cerceve

    def buton_tiklama(self, fare_x, fare_y):
        for d_index, dugme_degeri in self.dugmeler.items():
            (x, y, sag_x, alt_y) = dugme_degeri["pozisyon"]
            aktif = dugme_degeri["aktif"]
            alan = [(x, y), (sag_x, y), (sag_x, alt_y), (x, alt_y)]

            icinde = cv2.pointPolygonTest(np.array(alan, np.int32), (int(fare_x), int(fare_y)), False)
            if icinde > 0:
                print("AKTİF mi?", aktif)
                yeni_durum = False if aktif is True else True
                self.dugmeler[d_index]["aktif"] = yeni_durum

    def aktif_buton_listesi(self):
        aktif_liste = []
        for d_index, dugme_degeri in self.dugmeler.items():
            aktif = dugme_degeri["aktif"]
            metin = dugme_degeri["metin"]
            if aktif:
                aktif_liste.append(str(metin).lower())

        return aktif_liste
