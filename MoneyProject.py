import cv2
import os
import numpy as np


threshold = 15
path = 'ImagesQuery'
orb = cv2.ORB_create(nfeatures=1000)

images = []
kernel = np.ones((5, 5), np.uint8)
ClassNames = []
myList = os.listdir(path)
print("Total Classes Detected", len(myList))
for cl in myList:
    imgCur = cv2.imread(f"{path}/{cl}", 0)
    images.append(imgCur)
    ClassNames.append(os.path.splitext(cl)[0])
print(ClassNames)


def findDes(images):
    desList = []
    for img in images:
        kp, des = orb.detectAndCompute(img, None)
        desList.append(des)
    return desList


def findID(img, deslist):
    kp2, des2 = orb.detectAndCompute(img, None)
    bf = cv2.BFMatcher()
    matchlist = []
    finalvalue = -1
    try:
        for des in deslist:
            matches = bf.knnMatch(des, des2, k=2)
            good = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append([m])
            matchlist.append(len(good))
    except:
        pass
    if len(matchlist) != 0:
        if max(matchlist) > threshold:
            finalvalue = matchlist.index(max(matchlist))
    return finalvalue   



def get_contours(img):
    img_blur = cv2.GaussianBlur(img2, (7, 7), 1) # Making the image blurry
    img_edges = cv2.Canny(img_blur, 30, 30) # Finding the edges in the image for detecting where the image is.
    img_dialation = cv2.dilate(img_edges, kernel, iterations=1) # Dilating our image so that the edges detected by canny edge detector can be made thick.
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # Detecting the contours(shapes)
    for cnt in contours:
        area = cv2.contourArea(cnt) # checking the area of contours
        if area > 5000: # there can be many countours so we are filtering it as our money area is large
            peri = cv2.arcLength(cnt, True) # Calculating our countour perimeter
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True) # performimg an approximation of a shape of a contour.
            x, y, w, h = cv2.boundingRect(approx) # finding the x, y coordinates and height and width of our money 
            final_img = imgOriginal[y: y + h, x: x + w] # Croping our image to get money only
            return final_img # returning our final image
        else:
            return img # returning our img2 image if the money is not detected and this situation comes when your image contains only money i.e. their is no any background.




desList = findDes(images)
print(len(desList))
img2 = cv2.imread("test/20 euro.jpg") # Reading the image. Change the name according to your img name


imgOriginal = img2.copy()
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
final_img = get_contours(img2) # Calling that function

X = findID(final_img, desList)
if X!=-1:
    cv2.putText(imgOriginal, ClassNames[X], (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 3)

cv2.imshow("img2", imgOriginal)
cv2.waitKey(0)
