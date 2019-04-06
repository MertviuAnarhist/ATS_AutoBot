import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    new = cv2.inRange(hsv, (0, 145, 86), (78, 255, 173))
    new = cv2.blur(new, (5,5))
    maskEr=cv2.erode(new, None, iterations = 2)
    maskDi = cv2.dilate(maskEr, None, iterations = 1)

    #c = cv2.bitwise_and(frame, frame, mask = maskDi)
    contours = cv2.findContours(maskDi, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = contours[0]
    if contours:
        contours = sorted(contours, key = cv2.contourArea, reverse = True)
        cv2.drawContours(frame, contours, 0, (255,0,255),3)
        x, y, w, h = cv2.boundingRect(contours[0])
        cv2.rectangle(new, (x,y), (x+w, y+h), (0, 255, 0), 2)
        endImage = frame[y:y+h, x:x+w]
    cv2.imshow('n', endImage)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
