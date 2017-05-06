# _________________________________________________________________________________________________

from datetime import datetime
import matplotlib.pyplot as plt
import cv2
import sys
import pickle
import numpy

# _________________________________________________________________________________________________

# Setup SimpleBlobDetector parameters
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

        return imgout, 0.0

    else:
        kp = sorted(kp, key = lambda x: x.size, reverse = True)
        temp_f = 0.0

        for k in kp:
            avr = getAvrValue(imgin, k)
            temp_f += temp_conv(avr)

        temp_f = temp_f / len(kp)

        imgout = imgin

    return imgout, temp_f

def read_process_images(folderpath, picklename, outpickle, choose):
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

    temp_list = []
    for i in xrange(len(info_ts)):
        im_curr, temp_curr = detectBlob(jpgpath + info_ts[i][1])
        temp_list.append((info_ts[i][0], temp_curr))

    with open(outpickle, 'wb') as f:
        pickle.dump(temp_list, f)

# _________________________________________________________________________________________________

if __name__ == '__main__':
    folder_path = sys.argv[1]
    info_pickle_fname = sys.argv[2]
    l_or_r = sys.argv[3]    # 0 = left, 1 = right
    out_pickle_fname = sys.argv[4]
    
    read_process_images(folderpath = folder_path,
                picklename = info_pickle_fname,
                outpickle = out_pickle_fname,
                choose = int(l_or_r))

# _________________________________________________________________________________________________

