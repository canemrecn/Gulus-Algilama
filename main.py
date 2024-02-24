import cv2
#OpenCV (cv2) kütüphanesini içe aktarır.
yuzCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
gulCascade = cv2.CascadeClassifier('Cascades/haarcascade_smile.xml')
#Cascade sınıflandırıcıları için eğitilmiş XML dosyalarını yükler. Bir tanesi yüzleri tespit
# etmek için ("haarcascade_frontalface_default.xml") diğeri ise gülümsemeleri tespit etmek
# için ("haarcascade_smile.xml") kullanılır.
kamera = cv2.VideoCapture(1)
#Kamerayı açar. 1, bilgisayarınızda mevcut olan ikinci kamerayı seçer. Eğer sadece bir
# kameranız varsa, 0 olarak değiştirmeniz gerekebilir.
kamera.set(3,1280) # genişlik # 640
kamera.set(4,720) # yükseklik # 480
#Kamera çözünürlüğünü ayarlar. Bu durumda, genişlik 1280 piksel, yükseklik 720 piksel
# olarak ayarlanır.
dosyaad = None
kaydedici = None
#Video kaydetme işlemi için kullanılacak dosya adı (dosyaad) ve kaydedici nesnesi
# (kaydedici) için başlangıç değerlerini atanır.
while True:
    _, kare = kamera.read()
#Kameradan bir kare okur. _ değişkeni, okunan değeri atlamak için kullanılır.
    gri = cv2.cvtColor(kare, cv2.COLOR_BGR2GRAY)
#Okunan kareyi gri tonlamalıye dönüştürür.
    yuzler = yuzCascade.detectMultiScale(
        gri,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (30, 30)
    )
#Yüzleri tespit etmek için Cascade sınıflandırıcısını kullanarak kareyi tarama yapar.
# Tespit edilen yüzlerin koordinatlarını yuzler değişkeninde saklar.
    for (x,y,w,h) in yuzler:
        cv2.rectangle(kare,(x, y), (x+w, y+h), (255,0,0),2)
        gri_kutu = gri[y:y+h, x:x+w]
        renkli_kutu = kare[y:y+h, x:x+w]
        gulusler = gulCascade.detectMultiScale(
            gri_kutu,
            scaleFactor = 1.5,
            minNeighbors = 18,
            minSize = (30, 30)
        )
        for (sx, sy, sw, sh) in gulusler:
            cv2.rectangle(renkli_kutu, (sx, sy), (sx + sw, sy + sh), (0, 0, 255),2)
#Tespit edilen yüzlerin üzerine dikdörtgen çizilir. Ardından, yüz bölgesini kare ve gri
# versiyonları olarak ayırır. Yüzün içindeki gülümsemeleri tespit etmek için gülümseme
# sınıflandırıcısını kullanır ve gülümsemelerin üzerine dikdörtgen çizer.
    cv2.imshow('kare', kare)
#Sonuç karesini görüntüler.
    if kaydedici is None and dosyaad is not None:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') # .mp4
        kaydedici = cv2.VideoWriter(dosyaad, fourcc, 24.0, (kare.shape[1], kare.shape[0]),True)
#Video kaydedici (kaydedici) henüz başlatılmamışsa ve bir dosya adı (dosyaad) belirtilmişse,
# kaydediciyi başlatır.
    if kaydedici is not None:
        kaydedici.write(kare)
#Kaydedici aktifse, kareleri kaydeder.
    k = cv2.waitKey(10) & 0xff
    if k == 27 or k == ord('q'):
        break
#Klavyeden bir tuşun basılıp basılmadığını kontrol eder. 'ESC' tuşuna veya 'q' tuşuna basıldığında
# döngüden çıkar ve programı sonlandırır.
kamera.release()
#Kamerayı serbest bırakır.
if kaydedici:
    kaydedici.release()
    cv2.destroyAllWindows()
#Kaydedici açıksa, kaydediciyi serbest bırakır ve pencereleri kapatır.