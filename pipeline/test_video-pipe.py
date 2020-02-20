#!/usr/bin/env python
# coding: utf-8
import cv2
import numpy as np
import os
import sys
import argparse
from datetime import datetime
import time
from predict import *


def extractImages(video_path):
    
    """Function to extract frames from input video of Ultrasound nerves"""

    FRAME_PATH = './images/test/'
    # Log the time
    time_start = time.time()
    # Start capturing the feed
    cap = cv2.VideoCapture(video_path)
    # Find the number of frames
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    print ("Number of frames: ", video_length)
    count = 0
    print ("Converting video..\n")
    # Start converting the video
    while cap.isOpened():
        # Extract the frame
        ret, frame = cap.read()
        # Write the results back to output location.
        cv2.imwrite(FRAME_PATH + "/%#05d.png" % (count+1), frame)
        count = count + 1
        # If there are no more frames left
        if (count > (video_length-1)):
            # Log the time again
            time_end = time.time()
            # Release the feed
            cap.release()
            # Print stats
            print ("Done extracting frames.\n%d frames extracted" % count)
            print ("It took %d seconds for conversion." % (time_end-time_start))
            break




def output_video():
    
    """Function to save segemented video"""
    
    image_folder = './images/predicted'
    video_name = 'output.avi'

    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 1, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))
    print('Segmentation Video Generated!')




def video_input(video_path = None):  
    """Function implements Segmented Pipeline from predict.py """

    # Create a VideoCapture object and read from input file
    DIR_PATH = os.getcwd()
    FILE_OUTPUT =  DIR_PATH + '/output/output.avi'

    if os.path.isfile(FILE_OUTPUT):
        os.remove(FILE_OUTPUT)
    cap = cv2.VideoCapture(video_path)
    extractImages(video_path) # Extract frames from images
   
    # Check if camera opened successfully
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
    # Read until video is completed
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))    
    while(cap.isOpened()):
        predict()
        output_video()
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        else: 
            break

    # When everything done, release the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()




def test_output_video():
    """Test Segmented Nerves output video with contours """

    # Create a VideoCapture object and read from input file
    cap = cv2.VideoCapture('output.avi')

    # Check if camera opened successfully
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")

    # Read until video is completed
    while(cap.isOpened()):
      # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow('Frame',frame)

        # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

      # Break the loop
        else: 
            break

    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()




def clear_files(mydir):
    """Clear Frames & clear Image Tree"""

    filelist = [ f for f in os.listdir(mydir) if f.endswith(".png") ]
    for f in filelist:
        os.remove(os.path.join(mydir, f))




#Function to execute
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("file_name", type=str, nargs='?', default='sample_video.mp4')
	args = parser.parse_args()
	start_time = datetime.now()
	video_path = args.file_name #Input argument
	video_input(video_path)
	clear_files("./images/test/")
	clear_files("./images/predicted/")
	clear_files("./images/mask_predicted/asm/")
	clear_files("./images/mask_predicted/scm/")
	clear_files("./images/mask_predicted/bp/")
	clear_files("./images/mask_predicted/msm/")
	print('Tree Cleaned!!')
	test_output_video()    
	end_time = datetime.now()
	print('Duration: {}'.format(end_time - start_time))

