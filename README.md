# Table of Contents
- [Research_Track 1_First_Assignment ](#Research_Track1_First_Assignment )
- [Installing and running](#Installing&running)
- [Exercise](#Exercise)
- [Troubleshooting](#Troubleshooting)
- [Robot_API](#Robot_API)
	- [Motors](##Motors)
	- [Grabber](##Grabber)
	- [Vision](##Vision)
- [Coding](#Coding)
	- [drive](##drive)
	- [turn](##turn)
	- [Gold_find](##Gold_find)
	- [Release_Loc_Find](##Release_Loc_Find)
	- [Gold_grab](##Gold_grab)
	- [Release_Grabbed_Gold](##Release_Grabbed_Gold)
	- [main](##main)



### Research_Track1_First_Assignment 

This is the first assignment of Research track 1. The goal of this assignment is to gather all the golden boxes in one location next to each other. The environemnt and the initial and final configuration and formation of the boxes can be seen in Figure 1 and Figure2.  The portable robot simulator is used for this assignment which is developed by [Student Robotics](https://studentrobotics.org). 

<figure>
    <img src="sr/First_Config.png">
    <figcaption>Figure1) First configuration of the robot and environment</figcaption>
</figure>

<figure>
    <img src="sr/Final_Config.png">
    <figcaption> Figure2)Final configuration of the robot and environment</figcaption>
</figure>


A flowchart showing the algorithm written for this assignment can be seen in Figure 3:

<figure>
    <img src="sr/Flowchart.png">
    <figcaption> Figure3) Flowchart of the algorithm</figcaption>
</figure>

Installing&running
----------------------
The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/). Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

## Exercise
-----------------------------

To run one or more scripts in the simulator, use `run.py`, passing it the file names. 

you can run the program with:

```bash
$ python2 run.py assignment.py
```

## Troubleshooting

When running `python run.py <file>`, you may be presented with an error: `ImportError: No module named 'robot'`. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:
* Find the location of srtools: `pip show sr.tools`
* Get the location. In my case this was `/usr/local/lib/python2.7/dist-packages`
* Create symlink: `ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/`


Robot_API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to that of the [SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```
Coding
----------------------
As mentioned above, the goal of this assignment is for the robot to put all the golden boxes next to each other. For this reason a few functions are defined to make the code more smooth and understandable.
At first two parameters are defined as thresholds. `a_th` and `d_th` are the angle and distance threshold, respectively. These parameters can help the robot know when it's close enough to the target so that it can grab the target.
An empty list named `GrabbedGold` is defined. The code corresponding to the relocated box is added to this list to help the robot understand which boxes are relocated and it can ignore them when searching for new boxes to grab.
The defined functions for this assignment are as follows:

- drive
- turn
- Gold_find()
- Release_Loc_Find()
- Gold_grab()
- Release_Grabbed_Gold()

Each function is described here and then the main code which uses all the functions for the goal is presented and described.

### drive ###

the drive(speed, seconds) function was created to allow the robot to move straight. It get two inputs: `speed` and `seconds`. It will move with the power `speed` for a duration of `seconds`. it can go forward, giving to `speed` parameter a positive value, or it can go backward giving to `speed` parameter a negative value.
- speed: the linear velocity that we want the robot to assume. 
- seconds: the amount of seconds we want to drive.

```python
def drive(speed, seconds):

	R.motors[0].m0.power = speed
	R.motors[0].m1.power = speed
	time.sleep(seconds)
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0
```

### turn ###

The turn(speed, seconds) functions give the robot the ability to spin around itself. It's done by giving the right and left motors equal speeds with different signs. It get two inputs: `speed` and `seconds`. It will move with the power `speed` for a duration of `seconds`.

```python
def turn(speed, seconds):

    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
```
### Gold_find ###

The function  `Gold_find()` looks for the closest golden box and returns its distance (`dist`), angle (`rot_y`), and code (`Code`) with respect to the robot as output. In this function, the robot looks for golden boxes which are not removed before (Their code is not in the `GrabbedGold` list). In case it does not find a golden box, the function returns `-1` as output for all three parameters. The code is as follows:

 ```python
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
```
### Release_Loc_Find ###

This function finds the closest drop location for the grabbed golden box. The drop location is the location of a box which was relocated before and put next to other golden boxes. This finction returns three outputs which are distance (`dist`), angle (`rot_y`), and code (`Code`) of the drop location with respect to the robot. In order to find the drop location, the function tries to find the code of the closest golden box which is also in the `GrabbedGold` list. The code for this function is as follows:

```python
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
```

### Gold_grab ###

This function makes the robot move towards the closest golden box and it stops when reaching close wnough to the target box.  `a_th` and `d_th` are used to define when the robot reahes its target. If the robot is close enough to the target (`dist <= d_th`) the function exits and waits for further instructions from the user. If the distance is bigger than `d_th` and `-a_th < rot_y < a_th` The robot moves forward to reach the box. If the case is non  of these two, the robot should turn right or left accordingly to decrease its angular difference with the target and then start moving towards it. 

```python
def Gold_grab():

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
```

### Release_Grabbed_Gold ###

The function `Release_Grabbed_Gold() ` helps the robot move toward the drop location for the box it grabbed. When the robot reaches the target location the fucntions exits and waits for the users instructions. The algorithm and the reasoning for this function is exactly like `Gold_grab`. the only difference is that in this function `Release_Loc_Find()` is used to find the drop location. The robot drops the box when it reaches `dist < d_th+0.2`. This value is added to `d_th` to avoid collision of the robot and the grabbed box with the box which is already at the target location.

```python
def Release_Grabbed_Gold():

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
```
### main ###

Having all the functions described in previous section, we can now describe the main code which makes the robot grab and relocate all the golden boxes until it gathers all boxes at one location. 
At first, the closest golden box is found. This box will be considered as the first reference box. Consequently, the next box will be droped where this reference box is dropped. But it might not be the reference location for all next boxes, as the robot tries to find the closest drop location.
There might be a case when the robot can not see a golden box around (`dist = -1`). In this case, the robot keeps turning and surching until it finds a golden box. The code for this section is described as follows:

```python

	dist,rot_y,Code= Gold_find() # The robot tries to find the closest golden box
	while dist == -1:  # In case the robot can not find a golden box, it keeps turning and surching until it fids one 
		print("I have to search more for a gold box!!")
		turn(5,2)
		dist , rot_y , Code = Gold_find()
```
After the box is found, the robot moves towards it by `Gold_grab()` and grabs the box using `R.grab()`. The box is dropped at a random location. After the box is dropped, its code is added to the `GrabbedGold` list. The robot moves backwards and turns to avoid collision with the dropped box:

```python

	Gold_grab()  
	R.grab()
	print("Just grabbed it")

	turn(-10,1.1)
	drive(10 , 19)
	R.release()
	print("Package Delivered")

	drive(-10 , 2)
	turn(30,2)

	GrabbedGold.append(Code)

```
Afterwise a while loop is defined to make the robot reach all the remaining boxes and gather them next to each other. After each box is dropped its code is added to the `GrabbedGold` list and a new search starts.

```python

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

```
[sr-api]: https://studentrobotics.org/docs/programming/sr/

