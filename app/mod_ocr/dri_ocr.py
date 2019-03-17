import numpy as np
import pytesseract
import argparse
import cv2
import re
from matplotlib import pyplot as plt
from skimage.filters.rank import median
from skimage.morphology import disk

img =cv2.imread('dri2.jpg')
img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# hsv_channels = cv2.split(img)

# rows = img.shape[0]
# cols = img.shape[1]

# for i in range(0, rows):
#     for j in range(0, cols):
#         h = hsv_channels[0][i][j]

#         if h > 90 and h < 130:
#             hsv_channels[2][i][j] = 255
#         else:
#             hsv_channels[2][i][j] = 0
# cv2.imshow("show", hsv_channels[0])
# cv2.imshow("show2", hsv_channels[2])
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
kernel = np.ones((1, 1), np.uint8)
img = cv2.dilate(img, kernel, iterations=1)
img = cv2.erode(img, kernel, iterations=1)

# Apply blur to smooth out the edges
img = cv2.GaussianBlur(img, (5, 5), 5)
# Apply threshold to get image with only b&w (binarization)

img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, 7)
img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
kernel = np.ones((1, 1), np.uint8)
img = cv2.dilate(img, kernel, iterations=1)
img = cv2.erode(img, kernel, iterations=1)
img = cv2.fastNlMeansDenoising(img,None,30.0,7,21)


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

# im2, contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(img, contours, -1, (0,255,0), 3)


cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 600,600)
# cv2.imshow('image',img)
cv2.imshow('image',noisy_image)
cv2.waitKey()
text = []
result = pytesseract.image_to_string(noisy_image, lang="eng")
# print(""+result)
text=result.split()
print(text)
text=[re.sub('[^a-zA-Z0-9/]+', '', _) for _ in text]
# print(text)
print('\n\n')
while("" in text) : 
    text.remove("")
print(text)
# index=text.index('Number')
listlen=len(text)
matchh=False

# def hasnumbers(textstr):
#     return any(char.isdigit() for char in textstr)

# for index in range(0,listlen):
#     if(text[index].isalnum()):
#         matchh = hasnumbers(text[index])
#     if(len(text[index])==10 and matchh):
#         pannum=text[index]
#     if(bool(re.search('^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$',str(text[index])))):
#         bdate=text[index]
#     else:
#         index=index+1
# name=input("Enter your name:")
# name_index=text.index(name)
# i=name_index
# Name=text[i]
# Middle_Name=text[i+1]
# Surname=text[i+2]
# print("Aadhar naumber:"+aadnum)
# print('Birthday:'+bdate)
# print('Name:'+Name)
# print('Middle name:'+Middle_Name)
# print('Surname:'+Surname)