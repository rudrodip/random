import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
import numpy as np
import math

cap = cv2.VideoCapture(0)

# resize
frameResizeFactor = 0.7

# width and height of video capture
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# warpped width and height
warpWidth = int(width)
warpHeight = int(height)

# selected points and points to transform
selectedPts = np.empty((0, 2), np.float32)
warppedPts = np.empty((0, 2), np.float32)

# if 4 points are selected, then warp should be true
warpTrue = False
# transformation matrix is None at initialization
matrix = None

# color finder
colorFinder = ColorFinder(False)
# hsv value
hsvVals = {"hmin": 139, "smin": 48, "vmin": 134, "hmax": 167, "smax": 255, "vmax": 253}


def getArea(x, y):
    global selectedPts, warpTrue, warpWidth, warpHeight, matrix
    x, y = int(x), int(y)
    if selectedPts.shape[0] <= 4:
        selectedPts = np.append(selectedPts, np.float32([[x, y]]), axis=0)
    if selectedPts.shape[0] >= 4:
        if matrix is None:
            getProportion()
            matrix = cv2.getPerspectiveTransform(selectedPts, warppedPts)
        warpTrue = True
    else:
        warpTrue = False


def drawCircles(pts, frame):
    for pt in pts[:4]:
        cv2.circle(frame, (int(pt[0]), int(pt[1])), 2, (0, 255, 0), -1)

def getProportion():
    global warpWidth, warpHeight, warppedPts
    pt1, pt2, pt3 = selectedPts[0], selectedPts[1], selectedPts[2]

    l1 = math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)
    l2 = math.sqrt((pt2[0] - pt3[0])**2 + (pt2[1] - pt3[1])**2)

    proportion = l1/l2

    warpHeight = int(l2 * 1.5)
    warpWidth = int(warpHeight * proportion)
    warppedPts = np.float32([[0, 0], [warpWidth, 0], [warpWidth, warpHeight], [0, warpHeight]])


# main loop
def getFrames():
    while True:
        success, frame = cap.read()
        warppedFrame = frame

        if not success:
            break
        else:
            drawCircles(selectedPts, frame)

            if warpTrue:
                warppedFrame = cv2.warpPerspective(frame, matrix, (warpWidth, warpHeight))
                warppedFrame = cv2.resize(warppedFrame, (0, 0), None, frameResizeFactor, frameResizeFactor)

                # color finder
                imageColor, mask = colorFinder.update(warppedFrame, hsvVals)
                warppedFrame, contours = cvzone.findContours(warppedFrame, mask, minArea=200)

                if contours:
                    cx, cy = contours[0]["center"]
                    cv2.circle(warppedFrame, (cx, cy), 5, (0, 255, 0), -1)

        ret, frame = cv2.imencode(".jpg", warppedFrame)
        frame = frame.tobytes()

        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
