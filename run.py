# Copyright (c) Kano Computing 2014
#
# This software may be used and distributed
# according to the terms of the GNU General Public License version 2, incorporated
# herein by reference.

#=====================================#
# Some tools we need before we start  #
#=====================================#
import cv2, picamera, io
import numpy as np
from datetime import datetime
import email_with_attachments as email_helper


def main():
    #============================================================#
    #                This is where the fun begins!               #
    #                                                            #  
    #  You can change all the settings below.                    # 
    #  Use your gmail username + password, but remember          #   
    #  that storing it in files isn't very safe!                 #
    #                                                            #
    #============================================================#



    #============================================================#
    # Email address the message will be sent from                #
    # e.g. your Gmail email address                              #
    #============================================================#

    username = 'your_email@gmail.com'  

    #============================================================#
    # The password for your email account.                       #
    # WARNING: THIS IS NOT STORED SECURELY.                      #
    #============================================================#

    password = 'password123'

    #============================================================#
    # Email address you want to send the picture to              #
    #============================================================#

    send_email = 'send_image_to@somewhere.co.uk'


    #============================================================#
    # Set how much movement you want there to be before taking   #
    # a photograph.                                              #
    #                  1 is high : 20 is low                     #
    #============================================================#
 
    trigger_level = 10

    #============================================================#
    # SMTP is what we use to send an email. You can leave this   #
    # if you are using Gmail.                                    #
    #============================================================#
    
    smtp_server_url = 'smtp.gmail.com'

    #============================================================#
    # Your email address if it's different from the one above.   #
    # Don't worry about this if you're using Gmail               #
    #============================================================#
    
    user_email = None 


    MotionDetector(send_email, username, password, smtp_server_url, user_email, trigger_level)

#=========================================================================================================#
#        The code below is what makes the magic happen! If you're interested, why not take a look?        #
#=========================================================================================================#


def stream_to_opencv(stream):
    # Construct a numpy array from the stream
    data = np.fromstring(stream.getvalue(), dtype=np.uint8)
    # "Decode" the image from the array, preserving colour
    image = cv2.imdecode(data, 1)
    # OpenCV returns an array with data in BGR order. If you want RGB instead
    # use the following...
    #image = image[:, :, ::-1]
    return image


class MotionDetector():
    def __init__(self, send_email, username, password, smtp_server_url, user_email=None, trigger_level=100):
        print 'initialising, please wait...'

        NUM_MOTION_FRAMES = 6

        self.NUM_MOTION_FRAMES = NUM_MOTION_FRAMES
        self.trigger_level = trigger_level

        with picamera.PiCamera() as camera:
            stream = io.BytesIO()
            camera.framerate = 42.1
            camera.resolution = (640, 480)

            motion = False

            for foo in camera.capture_continuous(stream, format='jpeg'):
                #start_time = datetime.now()

                # Truncate the stream to the current position (in case
                # prior iterations output a longer image)
                stream.truncate()
                stream.seek(0)

                if not motion:

                    # save last image if it exists
                    try:
                        motion_images = []
                        motion_images.append(opencv_image)
                    except:
                        pass

                    # get latest image
                    opencv_image = stream_to_opencv(stream)

                    # detect motion
                    detection_level = self.detect_motion(opencv_image)
                    motion = self.refire_rate_limit(detection_level)

                    if motion:
                        print 'motion detected !'
                        print 'saving images...'
                        time_stamp = datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
                        motion_images.append(opencv_image)
                        #
                        es = email_helper.EmailServer(username, password, smtp_server_url)
                        subject = 'MOTION CAPTURED!'
                        text = '''<b>Captured! {0}<br>
                                    <img src="cid:image0"><br><br>
                                    <img src="cid:image1"><br><br>
                                    <img src="cid:image2"><br><br>
                                    <img src="cid:image3"><br><br>
                                    <img src="cid:image4"><br><br>
                                    <img src="cid:image5"><br><br>
                                '''.format(time_stamp)
                        alternative_text = 'pictures from motion detected'
                        es.create_email(subject, text, alternative_text)
                elif motion:
                    motion_images.append(stream_to_opencv(stream))

                    if len(motion_images) >= NUM_MOTION_FRAMES:
                        for i, image in enumerate(motion_images):
                            image_filename = '{0} frame {1}.png'.format(time_stamp, i)
                            cv2.imwrite(image_filename, image)
                            # send images as email
                            es.attach_file_image(image_filename)
                        es.send_email(send_email)

                        motion = False
                        motion_images = []
                #print (datetime.now() - start_time).microseconds

    def detect_motion(self, image):
        resize_resolution = (640/8, 480/8)
        image = cv2.resize(image, resize_resolution)   # reduce image size

        # if self.avg1 doesn't exist, initialise
        try:
            self.avg1
        except:
            self.avg1 = np.float32(image)

        cv2.accumulateWeighted(image, self.avg1, 0.7)
        res1 = cv2.convertScaleAbs(self.avg1)
        difference = cv2.absdiff(res1, image)   # moving average - current_frame
        detection_level = np.sum(difference) / 1000
        return detection_level

    def refire_rate_limit(self, detection_level):
        REFIRE_TIME = 30    # seconds
        # initialisation
        try:
            self.last_alarm_time
        except:
            self.last_alarm_time = datetime.now()

        current_time = datetime.now()
        time_since_last_alarm = (current_time - self.last_alarm_time).seconds
        if time_since_last_alarm > REFIRE_TIME:
            print 'monitoring: level {0} (trigger level {1})'\
                .format(detection_level, self.trigger_level)
            if detection_level > self.trigger_level:
                self.last_alarm_time = current_time
                return True
        else:
            return False



if __name__ == '__main__':
    main()
