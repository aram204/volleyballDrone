import cv2
from cvzone.HandTrackingModule import HandDetector
from djitellopy import Tello
from time import time

left_right_velocity = 0
forward_backward_velocity = 0
up_down_velocity = 0
yaw_velocity = 0
detector = HandDetector(detectionCon = 0.8,maxHands = 1)
me = Tello()
me.connect()
print(me.get_battery())
me.streamoff()
me.streamon()
height = 580
width = 600
me.takeoff()
me.move("up",65)
count = 0
t1 = time()
flag  =False
while True:
    frame_read = me.get_frame_read()
    frame = frame_read.frame
    hands, img = detector.findHands(frame)



    forward_backward_velocity = 40

    if hands and hands[0]['bbox'][2]*hands[0]['bbox'][3]>=70000:
        t1 = time()
        flag = True


    if flag and time()-t1 < 1.55:
        yaw_velocity = 100
    elif flag and time()-t1 < 4:
        left_right_velocity = 15
        yaw_velocity = 0
    else:
        yaw_velocity = 0
        left_right_velocity = 0
        flag = False

    print(time()-t1)
    if time()-t1 >15:
        forward_backward_velocity = 0
        me.land()



    me.send_rc_control(left_right_velocity,forward_backward_velocity,up_down_velocity,yaw_velocity)
    cv2.imshow('img', img)
    cv2.waitKey(1)


    if cv2.waitKey(1) & cv2.waitKey(1) == 113:
        me.land()
        break
