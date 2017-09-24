import time
import numpy as np
import cv2

#cap = cv2.VideoCapture("http://127.0.0.1:8082/SeCrEt/320/240/")
cap = cv2.VideoCapture(-1)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    #print(ret)
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(1)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
