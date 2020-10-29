import cv2
import os
import pickle
import face_recognition
from django.http import HttpResponse
import base64
import json


def deleteFace(request, name):

    try:

        f = open("face_encodes.dat", "rb+")
        encodes = pickle.load(f)

    except:

        return HttpResponse("No records set yet!")

    if name not in encodes:

        return HttpResponse("Id not present!")

    encodes.pop(name)
    f.seek(0)
    pickle.dump(encodes, f)
    return HttpResponse(name + " Deleted Successfully!")


def changeID(request, originalID, newID):

    try:

        f = open("face_encodes.dat", "rb+")
        encodes = pickle.load(f)

    except:

        return HttpResponse("No records set yet!")

    if originalID not in encodes:

        return HttpResponse("Id not present!")

    temp = encodes[originalID]

    encodes.pop(originalID)

    encodes[newID] = temp

    f.seek(0)

    pickle.dump(encodes, f)

    return HttpResponse("ID changed successfully!")


def findExisting(image):

    try:

        f = open("face_encodes.dat", "rb+")
        encodes = pickle.load(f)

    except:

        f = open("face_encodes.dat", "wb")
        encodes = dict({})

    f.close()

    if len(encodes) == 0:

        return "No Faces Registered!"

    imgdata = base64.b64decode(image.replace('~', '/'))

    filename = 'some_image.png'

    with open(filename, 'wb') as f:
        f.write(imgdata)

    known_face_encodings = list(encodes.values())

    known_face_names = list(encodes.keys())

    rgb_small_frame = face_recognition.load_image_file("some_image.png")

    face_locations = face_recognition.face_locations(rgb_small_frame)

    top, right, bottom, left = face_locations[0] if len(
        face_locations) >= 1 else [0, 0, 0, 0]

    if top == 0 and right == 0 and bottom == 0 and left == 0:

        return (False, "Sorry face not found, Please try again!")

    else:

        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)

        face_names = []

        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding, tolerance=0.4)
            print("matches array", matches)
            name = "Unknown"

        # # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)

                name = known_face_names[first_match_index]

            face_names.append(name)

        if True not in matches:

            return (False, "No known face found, Maybe you want to register a new face.")

        return (True, str(len(face_names)) + " person(s) found in the photo: " + ", ".join(face_names))

    return (False, "No case encountered!")


def addNewFace(request, name):

    try:

        f = open("face_encodes.dat", "rb+")
        encodes = pickle.load(f)

    except:

        f = open("face_encodes.dat", "wb")
        encodes = dict({})

    image = str(request.body)[2:-1]

    doesExist = findExisting(image)

    if doesExist[0]:
        return HttpResponse("Face already registered with id(s): " + doesExist[1].split(':')[1].strip())

    imgdata = base64.b64decode(image.replace('~', '/'))

    filename = 'some_image.png'

    with open(filename, 'wb') as f1:
        f1.write(imgdata)

    rgb_small_frame = face_recognition.load_image_file("some_image.png")

    face_locations = face_recognition.face_locations(rgb_small_frame)

    if len(face_locations) > 1:

        return HttpResponse("More Than One Face Found, Please try again.")

    elif len(face_locations) == 0:

        return HttpResponse("Sorry face not found, Please try again!")

    else:

        # top, right, bottom, left = face_locations[0] if len(face_locations) >= 1 else [0,0,0,0]

        face_encoding = face_recognition.face_encodings(
            rgb_small_frame, face_locations)[0]

        encodes[name] = face_encoding

        f.seek(0)

        pickle.dump(encodes, f)

        f.close()

        return HttpResponse("Face encodings saved by the name: " + name)

    return HttpResponse("No case encountered!")


def recog(request):
    image = str(request.body)[2:-1]

    return HttpResponse(findExisting(image)[1])
