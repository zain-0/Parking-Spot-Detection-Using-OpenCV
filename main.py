import cv2
import numpy as np
from util import get_parking_spots_bboxes, empty_or_not, calc_diff

video_path='parking_crop.mp4'
mask='mask_crop.png'
mask = cv2.imread(mask,0)

connected_components = cv2.connectedComponentsWithStats(mask,4,cv2.CV_32S)
spots = get_parking_spots_bboxes(connected_components)

frame_nmr=0
prev_frame = None

step = 30 # Check every 30 frames
spots_status = [None for j in spots]
diffs = [None for j in spots]

cap = cv2.VideoCapture(video_path)

# Check if the video capture is open
if not cap.isOpened():
    print("Error: Unable to open video source")
    exit()

# Do something with the video capture, like reading frames
while True:
    ret, frame = cap.read()

    if frame_nmr % step == 0 and prev_frame is not None: # Capture every 30 frames
        
        for spot_index, spot in enumerate(spots):
                
                x1,y1,w,h = spot
                spot_crop = frame[y1:y1 + h,x1:x1+w, :]
                prev_crop= prev_frame[y1:y1 + h,x1:x1+w, :]
                diffs[spot_index] = calc_diff(spot_crop,prev_crop) # Diff between current and previous frame
    
    if frame_nmr % step == 0:

        if prev_frame is  None:
            toBeChecked = range(len(spots)) # For first 29 frames

        else:
            toBeChecked = [i for i in np.argsort(diffs) if diffs[i]/np.amax(diffs) > 0.4] # Diffrence more than 0.4 are needed to be checked
        
        for spot_index in toBeChecked:

            spot=spots[spot_index]
            x1,y1,w,h = spot
            spot_crop = frame[y1:y1 + h,x1:x1+w, :]
            spot_status = empty_or_not(spot_crop)   # Check if the "changed" spot is empty or not
            spots_status[spot_index] = spot_status

    if frame_nmr % step == 0:
       prev_frame = frame.copy()    
    
    for spot_index, spot in enumerate(spots):  # Printing the bboxes every frame
        
        spot_status = spots_status[spot_index]
        x1 , y1 , w , h = spots[spot_index]
        if spot_status:
          frame = cv2.rectangle(frame,(x1,y1),(x1+w,y1+h),(0,255,0),2)
        else:
          frame = cv2.rectangle(frame,(x1,y1),(x1+w,y1+h),(0,0,255),2)

    cv2.rectangle(frame, (80, 20), (550, 80), (0, 0, 0), -1)

    cv2.putText(frame, 'Available spots: {} / {}'.format(str(sum(spots_status)), str(len(spots_status))), (100, 60),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    
    cv2.imshow('frame',frame)
    # Exit loop if 'q' is pressed
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    frame_nmr += 1

# Release the video capture resources
cap.release()
cv2.DestroyAllWindows()