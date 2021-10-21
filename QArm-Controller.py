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

Purpose: This function assigns the drop off coordinate to the dropoff_location variable,
the locations are assigned depending upon the obj_ID which is passes into the
function as an argument

Author: Muneeb Shah
Last Update: December 1st, 2020
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

Purpose: This function controls the movement of the arm. If the right arm's sensor
signal is 1 then the arm will move to the approarite drop off location.
If the left arm sensor is between 0.5 and 0.75 then the arm will move to
the pick up location. This function return True if the initial if statemtne is True
else it will return False.

Author: Jibin Mathew
Last Update: December 1st, 2020
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

Purpose: This function control the operation of the gripper that is located at the end
of the arm. If both the left and right arm sensor value is equal to zero, then gripper
open and close. The gripper will open id the effectorOpen varible equal to Flase. The
gripper will close if the effectorOpen variable is equal to True.This function return True if the initial if statemtne is True
else it will return False.

Author: Muneeb Shah
Last Update: December 1st, 2020

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

Purpose: This functuion controls the operation of opening and closing the drawer, if the
left arm and right arm sensor values are between 0.25 and 0.5 then the code will check
to see what type of container the arm is dealing with. If it is a small container
then the drawers will remain closed. If it is big container then the program will
check to see if the drawer is open or closed, if the drawer is open the obj_ID will be 14,
15 or 16. Therefore, if obj_ID is equal to 14,15 or 16 the program will close the
drawer. This function return True if the initial if statemtne is True
else it will return False.

Author: Jibin Mathew
Last Update: December 1st, 2020

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

'''
Purpose:This for loop is like the main function, it calls the functions above in logical
order to execute different tasks. Each of the above functions are embedded in a
while loop to force the user to move the arm/arms to the desired value for the specific
operation. Each of the functions above returns True/False depending on the initial
if statement in the function. If the returned value is False the loop will continue, and 
if it is true then the code will exit the loop and move on to the next function.
If the program is dealing with a large container then the code will set the obj_ID
equal to the original value + 10 this new obj_ID will be used to close the container
in the open_drawer function

Author: Jibin Mathew and Muneeb Shah
Last Update: Decemeber 1st, 2020
'''
for i in range (1,7):
    effectorOpen = True #This variable lets the code know if the gripper is colsed or open.
    arm.home()
    time.sleep(1)
    arm.spawn_cage(i) #spawn new container be sanitized 
    time.sleep(2)
    
    #detecting the required autoclave and open the drawer if container is large
    while open_drawer(i) == False: #while loops used to force user to move the arm to the correct value
        open_drawer(i)
        time.sleep(2)
        print("Finding Autoclave") #This print function will act as a guide to when the user must change the arm's position

    #moving the end effector to pickup location
    while move_end_effector(i) == False: 
        move_end_effector(i)
        time.sleep(2)
        print("Pick up the container")

    #closing the gripper
    while control_gripper(effectorOpen) == False:
        control_gripper(effectorOpen)
        time.sleep(2)
        print("Close the Gripper")
    effectorOpen = False

    #moving arm to required drop off location
    while move_end_effector(i) == False:
        move_end_effector(i)
        time.sleep(2)
        print ("Move to Autoclave")

    #open the gripper
    while control_gripper(effectorOpen) == False:
        control_gripper(effectorOpen)
        time.sleep(2)
        print("Place the container")
    time.sleep(2)
    arm.home()

    #closing the drawer is container is large
    if (i == 4 or i == 5 or i ==6): # The drawers are open at this point 
        while open_drawer(i+10) == False: #therefore obj_ID is set to i+10
            open_drawer(i+10)
            time.sleep(2)
            print("Close the Drawer")
    time.sleep(1)
        




