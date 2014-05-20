Raspberrypi Spy Camera
======================

Turns a Raspberry Pi plus camera module into a intelligent 'spy camera'. If motion is detected, an email is sent to a chosen email address containing the pictures captured.

The motion detection is implemented using opencv's python bindings, which provides fast image processing. 


#### To install on a Rasbperry Pi running Kano OS
1. enable camera
  * `$ sudo kano-camera`
2. install picamera
  * `$ sudo pip install picamera`
3. install opencv python bindings
  * `sudo apt-get install python-opencv`
4. restart the Raspberry Pi in order to finish the camera enabling
  * `$ sudo reboot`

#### To install on a Rasbperry Pi running Raspbian
1. enable camera in raspi-config
  * `$ sudo raspi-config`
2. install picamera (ensure you have python pip installed)
  * `$ sudo pip install picamera`
3. install opencv python bindings
  * `sudo apt-get install python-opencv`
4. restart the Raspberry Pi in order to finish the camera enabling
  * `$ sudo reboot`

#### How to use 
1. edit motion_detection.py, scroll to the bottom, edit email/smpt_server details
2. run the motion_detection.py in python
  * `$ python motion_detection.py 'my_password'`
