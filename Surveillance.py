#import libraries
import os
import cv2
import numpy as np
import face_recognition
from imutils import paths
from datetime import datetime

dtt=str (datetime.now().strftime('%d-%m-%Y  %H;%M;%S'))                 #Load current date and time
filename= dtt + " .avi"                                                 #make filename for stored video

path=r'/home/hasan/Desktop/moiz_proj/Surveillance/s_DATA'              #path for the dataset for respective batches,sections
os.chdir(path)                                                          #change current directory to the above mentioned path

known_people_names=[f.name for f in os.scandir(path) if f.is_dir() ]  #load the labels of folder in specified path
imagePaths = sorted(list(paths.list_images(path)))
known_people_encodings=[]                                               #initialize array for storing encodings of people in dataset
for imagePath in imagePaths:                                            #iterate through each image path and load encodings
        face = face_recognition.load_image_file(imagePath)
        faces_encoding = face_recognition.face_encodings(face)[0]
        known_people_encodings.append(faces_encoding)

os.chdir(r"/home/hasan/Desktop/moiz_proj/Surveillance")           #change directory to loaction where video will be stored
video_capture = cv2.VideoCapture(0)                                     #initialize video capturing
fourcc=cv2.VideoWriter_fourcc(*'XVID')                                  #sets the video codecs that is about to be saved
out=cv2.VideoWriter(filename,fourcc,24.0,(640,480))                     #sets the filename,type,fps,resolution of the video


# Initialize some variables
face_locations = []
face_encodingss = []
face_names = []
use_frame = True                                                        #flag to skip every alternate frame
match=[]                                                        #list to store the names of people present
size=len(known_people_names)
while True:                                                             #loop over each frame to make continous video
    
    ret, frame = video_capture.read()                                   #Grab a single frame of video
    out.write(frame)                                                    #write the recorded surveillance video
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)             #Resize frame of video to half the size for faster processing
    r_frame = small_frame[:, :, ::-1]                                   #Convert the image from BGR color format to RGB color format...
                                                                   
    
    if use_frame:                                                       #processes every alternate frame of video
        
        face_locations = face_recognition.face_locations(r_frame)       #Find the loaction of all facessin the current frame
        face_encodingss =face_recognition.face_encodings(r_frame,face_locations) #find encodings of all faces located

        face_names = []
        for face_encoding in face_encodingss:                           #loop over every encoding
            
            matches = face_recognition.compare_faces(known_people_encodings, face_encoding) #See if the face matches 
            name = "Unknown"                                            #set default detected name to "UNKNOWN"
            
            if True in matches:
                start=0
                end=3 
                for x in range(size):                #iterate through each label
                    for y in range(start,end):       #each label has 3 images so iterate through start-end
                        match.append(matches[y])      #and append them        

                    
                    if match.count(True)<3:         #set threshold for accuracy, 3 means all should be true
                        start+=3                    #if all are not true then update start and end pointers
                        end+=3                      
                        match=[]                    #empty previous data
                        name = "Unknown"

                    elif match.count(True)==3:      #if a match is found find the label
                        match_index =x
                        name = known_people_names[match_index]#load name from known people name
                        match=[]
                        break      #break the loop
        
            face_names.append(name)                                     #append the names of the people detected

    use_frame = not use_frame                                           #change the flag to skip/use the next frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 2                                                        # Scale back up face locations by x 2
        bottom *= 2
        left *= 2
        right*=2

        
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2) # Draw a rectangle around the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)# Draw a label with a name below the face
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'ESC' on the keyboard to quit!
    if cv2.waitKey(1) == 27:
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
