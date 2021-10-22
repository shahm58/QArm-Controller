import sys
sys.path.append('../')

from Common_Libraries.p2_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim ():
    try:
        arm.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

arm = qarm()

update_thread = repeating_timer(2, update_sim)

pickup = [0.4932, 0.0034, 0.0366]
reset = [0.4064,0.0,0.4826]

'''
Function: id_autoclavebin_location(parameter)
Parameter: obj_ID
Return type: Boolean
'''
def id_autoclavebin_location(obj_ID):
    if obj_ID == 1: #small red 
        dropoff_location = [-0.5884, 0.2359, 0.3711] 
    elif obj_ID == 2: #small green
        dropoff_location = [-0.0006, -0.6238, 0.3718] 
    elif obj_ID == 3: #small blue
        dropoff_location = [0.0011, 0.6238, 0.3718] 
    elif obj_ID == 4: #big red
        dropoff_location = [-0.3459,0.1398,0.216]
    elif obj_ID == 5: #big green
        dropoff_location = [0.0,-0.3731,0.216]
    elif obj_ID == 6: #big blue
        dropoff_location = [0.0,0.3731,0.216]
    else:
        dropoff_location = [0.4064,0.0,0.4826]
    return dropoff_location

'''
Function: move_end_effector(parameter)
Parameter: obj_ID
Return type: Boolean
'''
def move_end_effector(obj_ID):
    if  arm.emg_right() == 1:
        arm.move_arm(reset[0],reset[1],reset[2])
        time.sleep(2)
        moveEnd = id_autoclavebin_location(obj_ID)
        time.sleep(2)
        arm.move_arm(moveEnd[0],moveEnd[1],0.4826)
        time.sleep(1)
        arm.move_arm(moveEnd[0],moveEnd[1],moveEnd[2])
        time.sleep(2)
        return True
    elif arm.emg_left() > 0.5 and arm.emg_left() < 0.75:
        arm.home()
        time.sleep(2)
        arm.move_arm(pickup[0],pickup[1],pickup[2])
        time.sleep(2)
        return True
    else:
        return False

'''
Function: control_gripper(parameter)
Parameter: effectorOpen
Return type: Boolean
'''
def control_gripper(effectorOpen):
    if arm.emg_left()  == 0 and arm.emg_right() == 0:
        print (effectorOpen)
        if effectorOpen == False:
            arm.control_gripper(-31)
        elif effectorOpen == True:
            arm.control_gripper(31)
        return True
    else:
        return False
    
'''
Function: open_drawer(parameter)
Parameter: obj_ID
Return type: Boolean
'''            
def open_drawer(obj_ID):
    if arm.emg_left() > 0.25 and arm.emg_left() < 0.5 and arm.emg_right() > 0.25 and arm.emg_right() < 0.5:
        if obj_ID == 4:
            arm.open_red_autoclave(True)
            return True
        elif obj_ID == 5:
            arm.open_green_autoclave(True)
            return True
        elif obj_ID == 6:
            arm.open_blue_autoclave(True)
            return True
        elif obj_ID == 14 or obj_ID == 15 or obj_ID == 16:
            arm.open_red_autoclave(False)
            arm.open_green_autoclave(False)
            arm.open_blue_autoclave(False)
            return True
        else:
            arm.open_red_autoclave(False)
            arm.open_green_autoclave(False)
            arm.open_blue_autoclave(False)
            return True
    
    else:
        return False

for i in range (1,7):
    effectorOpen = True 
    arm.home()
    time.sleep(1)
    arm.spawn_cage(i)
    time.sleep(2)
        
    while open_drawer(i) == False: 
        open_drawer(i)
        time.sleep(2)
        print("Finding Autoclave") 

    while move_end_effector(i) == False: 
        move_end_effector(i)
        time.sleep(2)
        print("Pick up the container")

    while control_gripper(effectorOpen) == False:
        control_gripper(effectorOpen)
        time.sleep(2)
        print("Close the Gripper")
    effectorOpen = False

    while move_end_effector(i) == False:
        move_end_effector(i)
        time.sleep(2)
        print ("Move to Autoclave")

    while control_gripper(effectorOpen) == False:
        control_gripper(effectorOpen)
        time.sleep(2)
        print("Place the container")
    time.sleep(2)
    arm.home()

    if (i == 4 or i == 5 or i ==6): 
        while open_drawer(i+10) == False: 
            open_drawer(i+10)
            time.sleep(2)
            print("Close the Drawer")
    time.sleep(1)
        




