import cv2


#Import the cascades....
body_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


some_one =1
new_some_one = 1
changed = 1
frame_count = 0
#Displaying the image
video_capture = cv2.VideoCapture(0)
while True:
    if some_one == 1 and changed == 1:
        changed = 0
        print("Lights On")
    elif some_one == 0 and changed == 1:
        changed = 0
        print("Lights Off")
    #Getting the frames and the grayscale
    _, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #Get the co-ordinates for the humans

    people = body_cascade.detectMultiScale(gray, 1.1, 5) #the first one is the image, second is the scale and the last is the neighbours

    for (x,y,w,h) in people:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        
    if len(people) == 0:
        frame_count+= 1
    else:
        new_some_one = 1
        frame_count = 0
        
    if frame_count>10 :
        new_some_one = 0
        frame_count = 0
        
    if new_some_one != some_one:
        some_one = new_some_one
        changed = 1
        
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()
