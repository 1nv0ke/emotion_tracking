# _________________________________________________________________________________________________

from datetime import datetime
import matplotlib.pyplot as plt
import cv2
import sys
import pickle
import numpy as np

# _________________________________________________________________________________________________

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 80
params.maxThreshold = 200

# Filter by Area.
params.filterByArea = True
params.minArea = 3000
params.maxArea = 500000

params.filterByCircularity = False
params.filterByConvexity = False
params.filterByInertia = False
params.filterByColor = False

detector = cv2.SimpleBlobDetector(params)

# _________________________________________________________________________________________________

# Parameters setting
UPPER_BOUND_L = 400
LOWER_BOUND_L = 920
UPPER_BOUND_R = 400
LOWER_BOUND_R = 850

TEMP_RANGE_MIN = 27.0
TEMP_RANGE_MAX = 34.0

# _________________________________________________________________________________________________

def nothing(x):
    pass

def temp_conv(pixel_val):
    return float(pixel_val * (TEMP_RANGE_MAX - TEMP_RANGE_MIN) / 256 + TEMP_RANGE_MIN)
    
def getAvrValue(imgin, kp):
    total = 0
    count = 0
    for i in xrange(int(kp.size)):
        for j in xrange(int(kp.size)):
            posX = int(-kp.size / 2 + i + kp.pt[1])
            posY = int(-kp.size / 2 + j + kp.pt[0])

            # don't count out of area pixels
            if (posX >= 1536 or posX < 0):
                continue
            if (posY >= 2048 or posY < 0):
                continue

            pt = imgin[posX][posY]
            
            # only count pixels with value > 8
            # min pixel value on image = 8
            if pt > 8: 
                total += pt
                count += 1

    if count != 0:
        avr = total / count
    else:
        avr = 0

    return avr

def detectBlob(imgname):
    imgin = cv2.imread(imgname, cv2.IMREAD_GRAYSCALE)

    kp = detector.detect(imgin)

    # remove blobs out of bound & get biggest blob in bounding area
    for k in kp[:]:
        if (k.pt[1] < UPPER_BOUND or k.pt[1] > LOWER_BOUND):
            kp.remove(k)

    if len(kp) == 0:
        imgout = imgin
        cv2.line(imgout, (0, UPPER_BOUND), (2047, UPPER_BOUND), (255, 0, 0))
        cv2.line(imgout, (0, LOWER_BOUND), (2047, LOWER_BOUND), (255, 0, 0))
        return imgout, 0.0

    elif len(kp) == 1:
        k = kp[0]
        avr = getAvrValue(imgin, k)
        temp_f = temp_conv(avr)
        pos = (int(k.pt[0]), int(k.pt[1]))
        cv2.putText(imgin, "%.2f" % temp_f, pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0))

        avrPos = []

    else: # Number of keypoints > 1
        kp = sorted(kp, key=lambda x: x.size, reverse=True)
        kpNum = len(kp)
        avrPos = np.array([0.0, 0.0])

        # get temperature of blob
        for k in kp:
            avrPos += np.array([k.pt[0], k.pt[1]])
        avrPos = avrPos / kpNum

        left_kp = []
        left_t = 0.0
        right_kp = []
        right_t = 0.0
        onOneSide = True

        distanceThreshold = 20.0

        for k in kp: # check if blobs are too close to each other
            if (abs(k.pt[0] - avrPos[0]) > distanceThreshold):
                onOneSide = False
                break

        for k in kp:
            avr = getAvrValue(imgin, k)
            temp_f = temp_conv(avr)

            if (onOneSide == False):
                if (k.pt[0] < avrPos[0]): # on the left side
                    left_kp.append(k)
                    left_t += temp_f
                else: # on the right side
                    right_kp.append(k)
                    right_t += temp_f

            else:
                if (avrPos[0] <= 1023):
                    left_kp.append(k)
                    left_t += temp_f
                else:
                    right_kp.append(k)
                    right_t += temp_f

        # Print temperature of both side
        if (left_t > 0.0):
            pos = (int(left_kp[0].pt[0]), int(left_kp[0].pt[1]))
            cv2.putText(imgin, "L:%.2f" % (left_t/len(left_kp)), pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0))
        if (right_t > 0.0):
            pos = (int(right_kp[0].pt[0]), int(right_kp[0].pt[1]))
            cv2.putText(imgin, "R:%.2f" % (right_t/len(right_kp)), pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0))

    imgout = cv2.drawKeypoints(imgin, kp, None, (0,0,255), 4)

    cv2.line(imgout, (0,UPPER_BOUND), (2047,UPPER_BOUND), (255,0,0))
    cv2.line(imgout, (0,LOWER_BOUND), (2047,LOWER_BOUND), (255,0,0))

    if (avrPos != []):
        cv2.line(imgout, (int(avrPos[0]),0), (int(avrPos[0]),1535), (255,0,255))

    return imgout, temp_f

def read_process_images(folderpath, picklename, choose):
    global UPPER_BOUND, LOWER_BOUND
    if (choose == 0):
        # Read & process Left camera
        jpgpath = folderpath + 'left/jpg/'
        UPPER_BOUND = UPPER_BOUND_L
        LOWER_BOUND = LOWER_BOUND_L
        with open(folderpath + 'left/' + picklename + 'l.pickle', 'rb') as f:
            info_ts = pickle.load(f)
    elif (choose == 1):
        # Read & process Right camera
        jpgpath = folderpath + 'right/jpg/'
        UPPER_BOUND = UPPER_BOUND_R
        LOWER_BOUND = LOWER_BOUND_R
        with open(folderpath + 'right/' + picklename + 'r.pickle', 'rb') as f:
            info_ts = pickle.load(f)
    else:
        print "Wrong usage!"
        return

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 1280, 960)
    cv2.createTrackbar('frame#', 'image', 0, len(info_ts)-1, nothing)
    cv2.setTrackbarPos('frame#', 'image', 0)

    num = 0
    im, temp = detectBlob(jpgpath + info_ts[num][1])

    while(1):
        cv2.imshow('image', im)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
        
        old_num = num
        num = cv2.getTrackbarPos('frame#', 'image')
        if num != old_num:
            im, temp = detectBlob(jpgpath + info_ts[num][1])
            
    cv2.destroyAllWindows()

# _________________________________________________________________________________________________

if __name__ == '__main__':
    folder_path = sys.argv[1]
    info_pickle_fname = sys.argv[2]
    l_or_r = sys.argv[3]    # 0 = left, 1 = right

    # folder_path = '/media/seven/MyPassport/emt_data/04282017/dual/02/'
    # info_pickle_fname = 'dual_2_'
    # l_or_r = '1'
    
    read_process_images(folderpath = folder_path,
                picklename = info_pickle_fname,
                choose = int(l_or_r))

# _________________________________________________________________________________________________

