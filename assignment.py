   
from __future__ import print_function

import time
from sr.robot import *


a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

R = Robot()
""" instance of the class Robot"""

GrabbedGold = list()

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


	
def Gold_find():

	dist =100
	
	
	for Box in R.see():
	
		if Box.dist<dist and Box.info.marker_type == MARKER_TOKEN_GOLD and Box.info.code not in GrabbedGold:
		
			dist = Box.dist
			rot_y = Box.rot_y
			Code = Box.info.code
			
	if dist == 100:
	
		return -1 , -1 ,-1
	
	else:
		return dist, rot_y ,Code
		
def Release_Loc_Find():

	dist =100
	
	
	for Box in R.see():
	
		if Box.dist<dist and Box.info.marker_type == MARKER_TOKEN_GOLD and Box.info.code in GrabbedGold:
		
			dist = Box.dist
			rot_y = Box.rot_y
			Code = Box.info.code
			
	if dist == 100:
	
		return -1 , -1 ,-1
	
	else:
		return dist, rot_y ,Code
		

def Gold_grab():

	a = 1			
	while a:
	    dist, rot_y ,Code= Gold_find()  # we look for markers
	    
	    if dist <d_th: 
		print("Found a Gold one!")	 
		
		a = 0
	    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
		print("Going forward!.")
		drive(10, 0.5)
	    elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
		print("Left a bit...")
		turn(-2, 0.5)
	    elif rot_y > a_th:
		print("Right a bit...")
		turn(+2, 0.5)

def Release_Grabbed_Gold():

	a = 1			
	while a:
	    dist, rot_y ,Code= Release_Loc_Find()  # we look for markers
	    
	    if dist <d_th+0.2: 
		print("Found a drop location!")	 
		
		a = 0
	    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
		print("Going forward!.")
		drive(10, 0.5)
	    elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
		print("Left a bit...")
		turn(-2, 0.5)
	    elif rot_y > a_th:
		print("Right a bit...")
		turn(+2, 0.5)
			
		
			

	
def main():

	dist,rot_y,Code= Gold_find()
	while dist == -1:
		print("I have to search more for a gold box!!")
		turn(5,2)
		dist , rot_y , Code = Gold_find()
	Gold_grab()
	R.grab()
	print("Just grabbed it")
	drive(10 , 2)
	R.release()
	print("Package Delivered")
	drive(-10 , 2)
	turn(30,2)
	GrabbedGold.append(Code)
	
	while len(GrabbedGold)< 6:
			
		dist,rot_y,Code= Gold_find()
		while dist == -1:
			print("I have to search more for a gold box!!")
			turn(5,2)
			dist , rot_y , Code = Gold_find()
		Gold_grab()
		R.grab()
		print("Just grabbed it")
		Newdist,Newrot_y,NewCode = Release_Loc_Find()
		
		while Newdist == -1:
			print("I have to search more for a destination!!")
			turn(5,2)
			Newdist , Newrot_y , NewCode = Release_Loc_Find()
		Release_Grabbed_Gold()
		R.release()
		print("Package Delivered")
		drive(-10,2)
		turn(30,2)
		GrabbedGold.append(Code)
		
main()
		
		
		
	
	
	
	
	
	
	
	
