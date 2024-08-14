import cv2
import numpy as np
from nhan_dien import YoloDetect
from telegram_bot import TelegramBot
import os
import time
from threading import Thread
# token: 6752231619:AAFxmtm-YvdwlMCQAkRraKuGllvcui9JGx4
# link lấy id: https://api.telegram.org/bot[token]/getUpdates
def guiAnhSangTelegram(chat_id, photo, caption):
    bot.guiAnh(chat_id, photo,caption)

start = time.perf_counter_ns()
cua_so = 'image'
ve_da_giac = True
def click_chuot(event, x, y, param, toa_do):
    global ve_da_giac
    if event == cv2.EVENT_LBUTTONDOWN:
        if ve_da_giac:            
            toa_do.append((x, y))
def veDaGiac(img, toa_do, mau):
    for diem in toa_do:
        img = cv2.circle(img, diem, 2, (0, 255, 0), -1)
    img = cv2.polylines(img, [np.int32(toa_do)], False, mau, 2)
    return img
TOKEN = "6752231619:AAFxmtm-YvdwlMCQAkRraKuGllvcui9JGx4"
chat_id = 1476474149
chat_id_trang_beo = 6856490278
model = YoloDetect()
bot = TelegramBot(TOKEN)
cap = cv2.VideoCapture(0)
toa_do = []
xam_pham = False
nhan_dien = False
dem = 0
mau = (0, 255, 0)
while True:
    _, img = cap.read()
    img = veDaGiac(img, toa_do, mau)
    start = time.perf_counter_ns()
    if nhan_dien:
        
        img, list_doi_tuong, diem = model.nhanDien(img)
        xam_pham = model.check(np.int32(diem), toa_do)
        if xam_pham:
            duration = time.perf_counter_ns() - start
            duration = duration // 1000000
            mau = (0, 0, 255)
            img = cv2.putText(img, "PHAT HIEN XAM PHAM !!!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            if duration % 50 == 0:
                os.chdir(r'\anh_xam_pham')
                cv2.imwrite('xam_pham.png', img)
                thread1 = Thread(target=guiAnhSangTelegram, args=(chat_id, open(r'xam_pham.png', 'rb'), "CẢNH BÁO: CÓ XÂM PHẠM !!!"))
                thread1.start()
                dem = 1
        else:
            img = cv2.putText(img, "Binh thuong", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            mau = (0, 255, 0)
            if dem == 1:
                os.chdir(r'\anh_xam_pham')
                cv2.imwrite('khong_xam_pham.png', img)
                
                thread1 = Thread(target=guiAnhSangTelegram, args=(chat_id, open(r'khong_xam_pham.png', 'rb'), "KHÔNG CÓ XÂM PHẠM"))
                thread1.start()
                dem = 0
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('d'):
        toa_do.append(toa_do[0])
        ve_da_giac = False
        nhan_dien = True
    cv2.imshow(cua_so, img)
    cv2.setMouseCallback(cua_so, click_chuot, toa_do)
cap.release()
cv2.destroyAllWindows()