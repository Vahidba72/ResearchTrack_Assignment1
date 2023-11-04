""" Importing the required libraries """

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
""" A parameter defined to import the code of each box which is grabbed """

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

	"""
	Function to find the closest Golden Box with no elements in the list "GrabbedGold"
	
	Returns:
		
		dist (float): distance of the closest golden token (-1 if no token is detected)
		rot_y (float): angle between the robot and the golden token (-1 if no token is detected)
		Code (int): The code of the closest golden token (-1 if no golden token is detected)
		
	"""

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


	"""
	
	Function to find the closest box nearby (among the boxes that were previously grabbed and put next to each other) as a drop location
	It finds the closest box which is in the "GrabbedGold" list and takes the box it grabbed to the location
	It finds the closest one so it does not bump into the other boxes on its way
	
	Returns:
	
		dist (float): distance of the closest golden token (-1 if no token is detected)
		rot_y (float): angle between the robot and the golden token (-1 if no token is detected)
		Code (int): The code of the closest golden token (-1 if no golden token is detected)
	
	
	
	"""

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

	"""
	
	Function to move towards the closest box nearby ( The boxes that are not yet grabbed and moved)
	
	
	"""

	a = 1			
	while a:
	
	    dist, rot_y ,Code= Gold_find()  # we look for gold boxes
	    
	    if dist <= d_th: # if the robot is close enough to the box the while loop is stopped so it can grab the box 
		print("Found a Gold one!")	 
		
		a = 0
	    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token but not close, we go forward to reach it
		print("Going forward!.")
		drive(10, 0.5)
	    elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right until it's aligned
		print("Left a bit...")
		turn(-2, 0.5)
	    elif rot_y > a_th:
		print("Right a bit...")
		turn(+2, 0.5)

def Release_Grabbed_Gold():

	"""
	
	Function to move towards the closest drop location ( The closest box which was previously moved and relocated)
	
	
	"""

	a = 1			
	while a:
	    dist, rot_y ,Code= Release_Loc_Find()  # we look for closest gold box which was droped previously
	    
	    if dist <d_th+0.2:  # if the robot is close enough to the drop location the while loop is stopped so the robot can release the box
	    
	    # The value 0.2 is defined so that the robot releases the box it holds a small distance away from the target box
		print("Found a drop location!")	 
		
		a = 0
	    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the drop location, we go forward
		print("Going forward!.")
		drive(10, 0.5)
	    elif rot_y < -a_th: # if the robot is not well aligned with the drop location, we move it on the left or on the right
		print("Left a bit...")
		turn(-2, 0.5)
	    elif rot_y > a_th:
		print("Right a bit...")
		turn(+2, 0.5)
				

	
def main():

	dist,rot_y,Code= Gold_find() # The robot tries to find the closest golden box
	while dist == -1:  # In case the robot can not find a golden box, it keeps turning and surching until it fids one 
		print("I have to search more for a gold box!!")
		turn(5,2)
		dist , rot_y , Code = Gold_find()
	
	# The robot moves toward the closest golden box and grabs it
	Gold_grab()  
	R.grab()
	print("Just grabbed it")
	
	# The robot turns and moves forward to a random drop location and releases the box
	turn(-10,1.1)
	drive(10 , 19)
	R.release()
	print("Package Delivered")
	
	# The robot moves backward a little to avoid hitting the box it dropped and turns 360 degrees to start looking for a new box
	drive(-10 , 2)
	turn(30,2)
	
	#The code of the box that was just dropped is added to the list so that the robot looks for other boxes in the next steps

	GrabbedGold.append(Code)
	
	# The robot starts a search, grab, drop algorithm and keeps doing it until all boxes are next to each other (GrabbedGold has the code of all boxes and its
	# length is 6)
	while len(GrabbedGold)< 6:
		
		# The robot moves toward the closest golden box and grabs it
		dist,rot_y,Code= Gold_find()
		while dist == -1:
			print("I have to search more for a gold box!!")
			turn(5,2)
			dist , rot_y , Code = Gold_find()
		Gold_grab()
		R.grab()
		print("Just grabbed it")
		
		# The robot finds a drop location for the box it's holding
		Newdist,Newrot_y,NewCode = Release_Loc_Find()
		
		# The robot keeps turning until it finds the group of boxes that were put together before and bribgs the box there
		# for the first round of the loop it brings the box to the reference box which was initially moved
		while Newdist == -1:
			print("I have to search more for a destination!!")
			turn(5,2)
			Newdist , Newrot_y , NewCode = Release_Loc_Find()
		Release_Grabbed_Gold()
		R.release()
		print("Package Delivered")
		drive(-10,2)
		turn(30,2)
		
		# The code of the dropped box is added to the List before starting a new search and grap 
		GrabbedGold.append(Code)
		
main()
		
		
		
	
	
	
	
	
	
	
	
