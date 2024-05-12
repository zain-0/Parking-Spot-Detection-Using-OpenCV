import cv2
import numpy as np
from util import get_parking_spots_bboxes, empty_or_not

video_path='parking_crop.mp4'
mask='mask_crop.png'
mask = cv2.imread(mask,0)

connected_components = cv2.connectedComponentsWithStats(mask,4,cv2.CV_32S)
spots = get_parking_spots_bboxes(connected_components)
frame_nmr=0
step = 30
spots_status = [None for j in spots]
# Open the video capture device or file
cap = cv2.VideoCapture(video_path)

# Check if the video capture is open
if not cap.isOpened():
    print("Error: Unable to open video source")
    exit()

# Do something with the video capture, like reading frames
while True:
    ret, frame = cap.read()
    if frame_nmr % step == 0:  # Capture every 30 frames
      for spot_index, spot in enumerate(spots):
        x1,y1,w,h = spot

        spot_crop = frame[y1:y1 + h,x1:x1+w, :]

        spot_status = empty_or_not(spot_crop)

        spots_status[spot_index] = spot_status

    for spot_index, spot in enumerate(spots):
        spot_status = spots_status[spot_index]
        x1 , y1 , w , h = spots[spot_index]
        if spot_status:
          frame = cv2.rectangle(frame,(x1,y1),(x1+w,y1+h),(0,255,0),2)
        else:
          frame = cv2.rectangle(frame,(x1,y1),(x1+w,y1+h),(0,0,255),2)
    if not ret:
        break
    # Check if frame is not None before displaying it
    if frame is not None:
        # Process the frame
        cv2.imshow('frame',frame)
    # Exit loop if 'q' is pressed
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    frame_nmr += 1

# Release the video capture resources
cap.release()
