import cv2
import numpy as np
import pickle
from skimage.transform import resize
MODEL = pickle.load(open('model.p','rb'))

def get_parking_spots_bboxes(connected_components):
  (totalLabels, label_ids, values, centroids) = connected_components

  slots = []
  coef = 1
  for i in range(1,totalLabels):
    x1 = int(values[i, cv2.CC_STAT_LEFT] * coef)
    y1 = int(values[i, cv2.CC_STAT_TOP] * coef)
    w = int(values[i, cv2.CC_STAT_WIDTH] * coef)
    h = int(values[i, cv2.CC_STAT_HEIGHT] * coef)
    slots.append((x1,y1,w,h))
  return slots

def empty_or_not(spot_bgr):
  flat_data=[]
  img_reiszed = resize(spot_bgr,(15,15,3))
  flat_data.append(img_reiszed.flatten())
  flat_data= np.array(flat_data)
  y_output=MODEL.predict(flat_data)
  if y_output == 0:
    return True
  else:
    return False
  
def calc_diff(im1,im2):
  return np.abs(np.mean(im1) - np.mean(im2))
