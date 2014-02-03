#!/usr/bin/python2

import logging
import cv
import numpy as np
import time

# Bool to define wether to capture the cam or not
capture = True
# Bool to define wether to show the capture stream or not
showStream = True
white_threshold = 15.0
checked = np.zeros((1, 1), dtype=np.int)
mat = np.zeros((1, 1))
clusters = []
balances = []


def capture(camNumber, showStream):
    # Open stream for that camera
    logging.info('Capture from camera #%d', camNumber)
    cam = cv.CaptureFromCAM(int(camNumber))
    # Stream to output window as long as it is active
    return cam
    while capture:
        stream = cv.QueryFrame(cam)
        if showStream:
            cv.ShowImage("Americium 241", stream)


def set_capture(onOrOff):
    if onOrOff == bool:
        global capture
        capture = onOrOff


def frame_to_mat(img):
    cv.Smooth(img, img, cv.CV_GAUSSIAN, 3, 0)
    mat = cv.GetMat(img)
    frame_values = np.asarray(mat)
    return frame_values


# Convert a bgr matrix to grayscale
def bgr2gray(mat):
    b, g, r = mat[:, :, 0], mat[:, :, 1], mat[:, :, 2]
    gray = 0.1140 * b + 0.5870 * g + 0.2989 * r
    return gray


# Find a white dot in the black input matrix
def harvest_entropy(mat_input):
    global mat
    global checked
    global clusters
    global balances
    mat = mat_input.copy()
    if np.ndim(mat) >= 2:
        # Create array to hold the already checked pixels
        checked = np.zeros((len(mat), len(mat[0])), dtype=np.int)
        # Traverse the grayscale values in search of a bright pixel
        for i in range(0, len(mat) - 1):
            for j in range(0, len(mat[0]) - 1):
                # Check if it hasn't been checked yet
                if (checked[i][j] != 1):
                    # Find clusters, if the pixel is above threshold
                    if (mat[i][j] >= white_threshold):
                        #print "Hit above white threshold"
                        # Add a new cluster to the list of clusters
                        cluster = []
                        clusters.append(cluster)
                        # Find the rest of the cluster
                        find_cluster(i, j)
                        #print "Number at: %dx%dpx : %s" % (j, i, mat[i][j])
                checked[i][j] = 1
        # If there's one or more clusters, calculate its or their balance point
        if len(clusters) > 0:
            balance_point = cluster_to_balance_point()
            logging.info('%s, %s', balance_point[1], balance_point[0])
            #print balance_point
            # Empty the global clusters variable again
            del clusters[:]
            balances.append([time.time(), balance_point])
            mean = mean_balances()
            logging.info('%s, %s (balance mean)', mean[1], mean[0])
            floats = coordinate_to_float(balance_point[0], balance_point[1])
            logging.info('%s, %s (float)', floats[1], floats[0])
            #return balance_point
            return floats
    else:
        logging.error('Input matrix has wrong dimension!')


# Find cluster around a non-black pixel
def find_cluster(x, y):
    global checked
    global mat
    global clusters
    # Append the current white dot to the last cluster
    dot = np.array([x, y, mat[x][y]])
    clusters[len(clusters) - 1].append(dot)
    # Search for surrounding white dots now
    # Search one pixel further right
    if (len(mat) - 1 >= (x + 1)) and (mat[x + 1][y] >= white_threshold) \
            and (checked[x + 1][y] != 1):
        find_cluster(x + 1, y)
    # Search one pixel further right and down
    if (len(mat) - 1 >= (x + 1)) and (len(mat[0]) - 1 >= y + 1) and \
            (mat[x + 1][y + 1] >= white_threshold) \
            and (checked[x + 1][y] != 1):
        find_cluster(x + 1, y + 1)
    # Search one pixel further down
    if (len(mat[0]) - 1 >= y + 1) and \
            (mat[x][y + 1] >= white_threshold) and (checked[x][y + 1] != 1):
        find_cluster(x, y + 1)
    # Search one pixel further down and further left
    if (len(mat[0]) - 1 >= y + 1) and x - 1 >= 0 \
            and (mat[x - 1][y + 1] >= white_threshold) \
            and (checked[x - 1][y + 1] != 1):
        find_cluster(x - 1, y + 1)
    # Add this pixel to the list of checked pixels
    checked[x][y] = 1


# Create balance point from cluster
# TODO: Make possible to choose only most significant cluster
def cluster_to_balance_point():
    global clusters
    cluster_balances = []
    x_balance = 0.0
    y_balance = 0.0
    for cluster in clusters:
        mean_x = 0.0
        mean_y = 0.0
        sum_total = 0.0
        for dot in cluster:
            # Calculate X balance (x * intensity)
            mean_x = mean_x + dot[0] * dot[2]
            # Calculate Y balance (y * intensity)
            mean_y = mean_y + dot[1] * dot[2]
            # Calculate Y total (all intensity summed up)
            sum_total = sum_total + dot[2]
        # Add up the balances and put them into a list
        cluster_x_balance = mean_x / sum_total
        cluster_y_balance = mean_y / sum_total
        cluster_balances.append([cluster_x_balance, cluster_y_balance])
    # If it's more than one cluster, balance between them
    if len(cluster_balances) > 1:
        logging.info('Balancing between a couple of clusters.')
        total_cluster_x_balance = 0.0
        total_cluster_y_balance = 0.0
        for balance in cluster_balances:
            total_cluster_x_balance = total_cluster_x_balance + balance[0]
            total_cluster_y_balance = total_cluster_y_balance + balance[1]
        x_balance = total_cluster_x_balance / float(len(cluster_balances))
        y_balance = total_cluster_y_balance / float(len(cluster_balances))
    else:
        logging.info('Balancing between one cluster.')
        x_balance = cluster_x_balance
        y_balance = cluster_y_balance
    return [x_balance, y_balance]


# Displays the mean balance calculated from all balances
def mean_balances():
    global balances
    mean_balance = [0.0, 0.0]
    for balance in balances:
        mean_balance[0] = mean_balance[0] + balance[1][0]
        mean_balance[1] = mean_balance[1] + balance[1][1]
    mean_balance[0] = mean_balance[0] / float(len(balances))
    mean_balance[1] = mean_balance[1] / float(len(balances))
    return mean_balance


# Calculates float value between 0.0 and 1.0 from coordinate
# TODO: insert on-the-fly mean_balance as parameter
def coordinate_to_float(x, y):
    global mat
    width = float(len(mat))
    height = float(len(mat[0]))
#    balance_dim = [width / 2, height / 2]
    floatx = x / width
    floaty = y / height
    return [floatx, floaty]
# TODO: Function to calculate floats from mean_balance on the fly
