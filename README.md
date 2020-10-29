# Face Recognition

A Basic Django application that checks for the faces in the snapshot and the recognizes the faces present inside it.

Used the facerecognition library for this purpose

Webpages are present inside this repository, the webcamTest1.html provides the option of searching and the addNew1.htm is used to register a new face to the face_encodes.dat file which is later read.

The process is to start webcam, position yourself and take a snapshot. It wil detect the number of people and label the unknown people as unknown and others with their name.

## Getting Started:

[ ] Clone the repository on your local system
[ ] Traverse to the root directory
[ ] Run `pip install -r requiredLibs.txt` to install the dependencies.
[ ] Run `python manage.py runserver` to start the server at port 8000
[ ] Open the webpages, and start using the app :) 