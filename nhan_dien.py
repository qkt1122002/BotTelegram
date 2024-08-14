from ultralytics import YOLO
from shapely.geometry import Point, Polygon
from ultralytics.utils.plotting import Annotator, colors
import cv2
import numpy as np


def veDoiTuong(results, img):
            class_ids = []
            annotator = Annotator(img, 3, results[0].names)
            boxes = results[0].boxes.xyxy.cpu()
            clss = results[0].boxes.cls.cpu().tolist()
            names = results[0].names
            for box, cls in zip(boxes, clss):
                class_ids.append(cls)
                annotator.box_label(box, label=names[int(cls)], color=colors(int(cls), True))
            return img, class_ids, boxes

class YoloDetect():
    def __init__(self, doi_tuong = "person", frame_width = 1200, frame_height = 720):
        self.doi_tuong = doi_tuong
        self.model = YOLO('yolov8n.pt')
        self.frame_width = frame_width
        self.frame_height = frame_height
        if self.doi_tuong == 'person':
              self.index = 0
        
    def nhanDien(self, frame):
        self.ket_qua = self.model.predict(frame)
        frame, class_id, boxes = veDoiTuong(self.ket_qua, frame)
        if self.index in class_id:
            diem = (boxes[0][0] + boxes[0][2]) // 2, (boxes[0][1] + boxes[0][3]) // 2
            frame = cv2.circle(frame,np.int32(diem), 5, (0, 255, 0), -1)
        else:
            diem = (0, 0)
            print('Khong co' + self.doi_tuong)  
        
        return frame, class_id, diem
    def check(self, point, polygon):
          da_giac = Polygon(polygon)
          diem = Point(point)
          is_inside = da_giac.contains(diem)
          return is_inside
# model = YoloDetect()
# cap = cv2.VideoCapture(0)

# while True:
#       _, img = cap.read()
#       img, class_id, diem = model.nhanDien(img)
      
#       cv2.imshow('img', img)
#       print(diem)
#       if cv2.waitKey(1) == ord('q'):
#             break
# cap.release()
# cv2.destroyAllWindows()