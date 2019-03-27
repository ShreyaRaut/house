import numpy as np
import pytesseract
import argparse
import cv2
import re
import math
from matplotlib import pyplot as plt
from skimage.filters.rank import median
from skimage.morphology import disk
from ..models import User
from ..forms import RegistrationForm
from flask_login import current_user


def scan(file):
    #Read the image 
    img =cv2.imread(file)

    #Resize it
    img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

    #Convert to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Erode and dilate it
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # Apply blur to smooth out the edges
    img = cv2.GaussianBlur(img, (5, 5), 9)

    # Apply threshold to get image with only b&w (binarization)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 27, 11)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    #Erode and dilate it again
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    #Remove the noise using opencv
    img = cv2.fastNlMeansDenoising(img,None,30.0,7,21)

    #Remove the noise using skimage for better result
    noisy_image = img
    noise = np.random.random(noisy_image.shape)
    noisy_image[noise > 10] = 255
    noisy_image[noise < -1] = 0

    fig, axes = plt.subplots(2, 2, figsize=(10, 10), sharex=True, sharey=True)
    ax = axes.ravel()

    ax[0].imshow(median(noisy_image, disk(1)), vmin=0, vmax=255, cmap=plt.cm.gray)
    ax[0].set_title('Median $r=1$')

    for a in ax:
        a.axis('off')

    #Show the image in a 600x600 window
    # cv2.namedWindow('image',cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('image', 600,600)
    # cv2.imshow('image',noisy_image)
    # cv2.waitKey()

    #Read the text from image and store it in a list
    text = []
    result = pytesseract.image_to_string(noisy_image, lang="eng")
    # print(noisy_image.shape)
    text=result.split()
    # print(text)

    #Remove useless special characters
    text=[re.sub('[^a-zA-Z0-9/]+', '', _) for _ in text]
    # print(text)

    #Remove empty strings from the list
    while("" in text) : 
        text.remove("")
    # print(text)

    #Find and store birthdate and gender
    listlen=len(text)
    Gender='male'
    for index in range(0,listlen):
        if(bool(re.search('^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$',str(text[index])))):
            bdate=text[index]
        if(text[index]=='Female'):
            Gender='Female'
        index=index+1

    #Crop the image to aadhar card number
    x,y=noisy_image.shape
    # print(""+str(x)+" "+str(y))
    y1=int(x/2)
    y2=int(y1/5)
    y1=y1 + int(y1/3)
    cropped = noisy_image[y1:x-y2, 0+100:y-100]

    #Show the cropped image
    # cv2.namedWindow('cropped',cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('cropped', 900,600)
    # cv2.imshow("cropped", cropped)
    # cv2.waitKey(0)

    #Extract aadhar number from cropped image and store it in a list
    aad = []
    res = pytesseract.image_to_string(cropped, lang="eng")
    aad=res.split()
    # print(aad)

    #Remove useless symbols
    aad=[re.sub('[^a-zA-Z0-9/]+', '', _) for _ in aad]
    # print('\n\n')

    #Remove empty strings from the list
    while("" in aad) : 
        aad.remove("")
    print(aad)

    #Form the aadhar number
    aadnum=''.join(aad)

    #Store Name,Middle name,Last name

    name=current_user.fname
    name_index=text.index(name)
    i=name_index
    Name=text[i]
    Middle_Name=text[i+1]
    Surname=text[i+1]

    print("Aadhar number:"+aadnum)
    print('Birthday:'+bdate)
    print('Name:'+Name)
    print('Middle name:'+Middle_Name)
    print('Surname:'+Surname)
    print('Gender:'+Gender)

    return Name,Middle_Name,Surname,bdate,Gender,aadnum
    