# #Modified by smartbuilds.io
# #Date: 27.09.20
# #Desc: This scrtipt script..

# import cv2 as cv

# from imutils.video import pivideostream
# from imutils.video.pivideostream import PiVideoStream
# import imutils 
# import time
# from datetime import datetime
# import numpy as np

# class VideoCamera(object):
#     def __init__(self, flip = False, file_type  = ".jpg", photo_string= "stream_photo"):
#         # self.vs = PiVideoStream(resolution=(1920, 1080), framerate=30).start()
#         self.vs = PiVideoStream().start()
#         self.flip = flip # Flip frame vertically
#         self.file_type = file_type # image type i.e. .jpg
#         self.photo_string = photo_string # Name to save the photo
#         time.sleep(2.0)

#     def __del__(self):
#         self.vs.stop()


#     def flip_if_needed(self, frame):
#         if self.flip:
#             return np.flip(frame, 0)
#         return frame

#     def get_frame(self):
#         frame = self.flip_if_needed(self.vs.read())
#         ret, jpeg = cv.imencode(self.file_type, frame)
#         self.previous_frame = jpeg
#         return jpeg.tobytes()

#     # Take a photo, called by camera button
#     def take_picture(self):
#         frame = self.flip_if_needed(self.vs.read())
#         ret, image = cv.imencode(self.file_type, frame)
#         today_date = datetime.now().strftime("%m%d%Y-%H%M%S") # get current time
#         cv.imwrite(str(self.photo_string + "_" + today_date + self.file_type), frame)
import time
import io
import threading
import picamera

class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera

    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (320, 240)
            camera.hflip = True
            camera.vflip = True

            # let camera warm up
            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # store frame
                stream.seek(0)
                cls.frame = stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

                # if there hasn't been any clients asking for frames in
                # the last 10 seconds stop the thread
                if time.time() - cls.last_access > 10:
                    break
        cls.thread = None