import cv2

cap = cv2.VideoCapture(0)
image = cv2.imread('test3.png')
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
image = cv2.inRange(image, (17, 54, 114), (84, 196, 152))
image = cv2.resize(image, (64,64))
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
        endImage = cv2.cvtColor(endImage, cv2.COLOR_BGR2HSV)
        endImage = cv2.inRange(endImage, (0, 145, 86), (78, 255, 173))
        endImage = cv2.resize(endImage, (64,64))
    val = 0
    for i in range(64):
        for j in range(64):
            if endImage[i][j] == image[i][j]:
                val = val+1
    if val > 2000:
        print("Это карта")
    else:
        print("Это не карта")
    cv2.imshow('n', endImage)
    cv2.imshow('s', image)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
