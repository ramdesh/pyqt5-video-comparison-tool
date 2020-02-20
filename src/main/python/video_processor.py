import cv2
import os
from datetime import datetime
import time
from model.predict import *


class VideoProcessor:
    def __init__(self, video_path):
        self.start_time = datetime.now()
        self.extract_images(video_path)

    def extract_images(self, video_path):
        """Function to extract frames from input video of Ultrasound nerves"""

        frame_path = os.getcwd() + '/images/frames/'
        # Log the time
        time_start = time.time()
        # Start capturing the feed
        cap = cv2.VideoCapture(video_path)
        # Find the number of frames
        video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
        print("Number of frames: ", video_length)
        count = 0
        print("Converting video..\n")
        # Start converting the video
        while cap.isOpened():
            # Extract the frame
            ret, frame = cap.read()
            # Write the results back to output location.
            cv2.imwrite(frame_path + "/%#05d.png" % (count + 1), frame)
            count = count + 1
            # If there are no more frames left
            if count > (video_length - 1):
                # Log the time again
                time_end = time.time()
                # Release the feed
                cap.release()
                # Print stats
                print("Done extracting frames.\n%d frames extracted" % count)
                print("It took %d seconds for conversion." % (time_end - time_start))
                print("Wrote frames to " + frame_path)
                break

    def stitch_video(self):
        """Function to save segemented video"""
        dir_path = os.getcwd()
        image_folder = dir_path + '/images/predicted'
        video_name = dir_path + '/output.avi'

        images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
        frame = cv2.imread(os.path.join(image_folder, images[0]))
        height, width, layers = frame.shape

        video = cv2.VideoWriter(video_name, 0, 1, (width, height))

        for image in images:
            video.write(cv2.imread(os.path.join(image_folder, image)))
        print('Segmentation Video Generated!')

    def run_model(self):
        predict()
        self.stitch_video()
        end_time = datetime.now()
        print('Duration: {}'.format(end_time - self.start_time))
        dir_path = os.getcwd()
        self.clear_files(dir_path + "/images/frames/")
        self.clear_files(dir_path + "/images/predicted/")
        self.clear_files(dir_path + "/images/mask_predicted/asm/")
        self.clear_files(dir_path + "/images/mask_predicted/scm/")
        self.clear_files(dir_path + "/images/mask_predicted/bp/")
        self.clear_files(dir_path + "/images/mask_predicted/msm/")
        return dir_path + '/output.avi'

    def clear_files(self, mydir):
        """Clear Frames & clear Image Tree"""

        filelist = [f for f in os.listdir(mydir) if f.endswith(".png")]
        for f in filelist:
            os.remove(os.path.join(mydir, f))
