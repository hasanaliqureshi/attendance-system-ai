#import libraries
import os
import cv2
import xlsxwriter
import numpy as np
import face_recognition
from imutils import paths
from datetime import datetime


date="Date:" + str(datetime.now().strftime('%d-%m-%Y'))                                  #Load current date
time="Time:" + str(datetime.now().strftime('%H;%M;%S'))                                  #Load current time
dtt= str(datetime.now().strftime('%d-%m-%Y  %H;%M;%S'))                                  #Load current date and time
filename= dtt + " .avi"                                                                  #make filename for stored video

pathss=r'C:\Users\moiz\Desktop\Project\Surveillance\15-16\A'                             #path for the dataset for respective batches,sections
os.chdir(pathss)                                                                         #change current directory to the above mentioned path

known_people_names=[f.name for f in os.scandir(pathss) if f.is_dir() ]  #load the labels of folder in specified path
imagePaths = sorted(list(paths.list_images(pathss)))
known_people_encodings=[]                                               #initialize array for storing encodings of people in dataset
for imagePath in imagePaths:                                            #iterate through each image path and load encodings
        face = face_recognition.load_image_file(imagePath)
        faces_encoding = face_recognition.face_encodings(face)[0]
        known_people_encodings.append(faces_encoding)


os.chdir(r"C:\Users\moiz\Desktop\Project\Surveillance\video")           #change directory to loaction where video will be stored
video_capture = cv2.VideoCapture(0)                                     #initialize video capturing
fourcc=cv2.VideoWriter_fourcc(*'XVID')                                  #sets the video codecs that is about to be saved
out=cv2.VideoWriter(filename,fourcc,24.0,(640,480))                     #sets the filename,type,fps,resolution of the video

# Initialize some variables
face_locations = []
face_encodingss = []
face_names = []
use_frame = True                                                         #flag to skip every alternate frame
presentNames=[]   #list to store the names of people present
match=[]                                                       
size=len(known_people_names)
att=['A' for x in range(size)]                                          #list to store the attendance of all people in dataset,Default absent 'A'

while True:                                                               #loop over each frame to make continous video
    
    ret, frame = video_capture.read()                                   #Grab a single frame of video
    out.write(frame)                                                    #write the recorded surveillance video
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)             #Resize frame of video to half the size for faster processing
    r_frame = small_frame[:, :, ::-1]                                   #Convert the image from BGR color format to RGB color format...

    if use_frame:                                                        #processes every alternate frame of video
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



    """# Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)"""

    
    for names in face_names:                                               #loop over the names in list 
        if names not in presentNames and names != 'Unknown':               #make sure no repitiation or "unknown" appends to list
            presentNames.append(names)

        else:
            pass    


    for pnames in presentNames:                                            #loop over the present names to extract the same index...
        ind=known_people_names.index(pnames)                                 #... in the known people names
        
        att[ind]='P'                                                       #mark attendance at that same index
    
    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'ESC' on the keyboard to quit!
    if cv2.waitKey(1) == 27:
        break

os.chdir(r"C:\Users\moiz\Desktop\Project\Surveillance\Attendance Record")#change the directory to the excel file of attendace storage loaction

sec="Section:"+str(pathss.split(os.path.sep)[-1])                          #extract the section from path provided
batch="Batch:" +str(pathss.split(os.path.sep)[-2])                         #extract the batch from path provided
excel=dtt+".xlsx"                                                          #set name of excel file to current date and time
workbook = xlsxwriter.Workbook(excel)                                      #initialize the worksheet
worksheet = workbook.add_worksheet()
worksheet.write('A1', date) 
worksheet.write('C1', time) 
worksheet.write('E1', batch) 
worksheet.write('G1', sec) 
worksheet.write('A3', 'Students') 
worksheet.write('C3', 'Attendance')
row = 4
column = 0

for f in known_people_names:                                               #print names of people in dataset into the list                                  
    worksheet.write(row, column,f)
    row += 1 

row = 4
column = 2

for a in att:                                                              #print attendance of people present/absent at same index
    worksheet.write(row, column,a)
    row += 1 

workbook.close()                                                           #close worksheet
# Release webcam
video_capture.release()
cv2.destroyAllWindows()
