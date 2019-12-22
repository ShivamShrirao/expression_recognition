#Importing the libraries first
from scipy.spatial import distance
import imutils
import dlib
import cv2
from imutils import face_utils



#Copy this fuction....it returns the acpect ration
def eye_aspect_ratio(eye):
    
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    
    ear = (A + B)/(2.0 * C)
    return ear


#Now, lets get the index of those eyes.....
(lstart, lend) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rstart, rend) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

#Lets make the detection and prediction objects
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#Now for the frames and the aspect ration threshold.....
frames_pass = 10
thresh = 0.25
#Just like we decided.......

cam = cv2.VideoCapture(0)
#To keep the track of the frames.....
flag = 0
while True:
    #Record the video...
    _, frame = cam.read()
    
    #Now, the usual stuff
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #Find the face in the grayscale image......
    faces = detect(gray, 0)
    
    for face in faces:
        #Getting the features form the face
        face = predict(gray, face)
        face = face_utils.shape_to_np(face)
        
        #Getting the points on for the left and the right eyes
        leftEye = face[lstart:lend]
        rightEye = face[rstart:rend]
        
        #Calculating the aspect ration for both the eyes
        leftEar = eye_aspect_ratio(leftEye)
        rightEar = eye_aspect_ratio(rightEye)
        
        #Finding the net aspect ration.....
        ear = (leftEar + rightEar)/2.0
        
        #Lets draw the convex hull for the sake of it.....it'll make it look cool....
        left_conv = cv2.convexHull(leftEye)
        right_conv = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [left_conv], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [right_conv], -1, (0, 255, 0), 1)
        
        #Now for the drowsyness detector part.....
        if ear < thresh:
            flag += 1
            
            if flag > frames_pass:
                #Alert the user if he is sleepy....
                
                cv2.putText(frame, "********ALERT*********",
                           (10, 30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "YOU ARE DROWSY",
                           (10, 324), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
        
            else:
                cv2.putText(frame, "AWAKE!!!",
                           (10, 324), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)

        
        else:
            #Reset the counted number of frames
            flag = 0 
    
    cv2.imshow("Live", frame)
   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cam.release()
cv2.destroyAllWindows()
