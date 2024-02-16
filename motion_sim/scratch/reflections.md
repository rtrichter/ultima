# Prototype 1
| Evolution # | Given Information    | Movement Controller  | Status        |
| ----------- | -------------------- | -------------------- | ------------- |
| 0           | Just boundaries      | give (x, y) position | Prototyped    |


# Libraries  

## External  
- numpy  
- cv2 (opencv-python)

## Native  
- enum.Enum
- time (visualization)
- json

# Things Learned
Images use indices img[y][x] NOT img[x][y]   
Be careful of units (especially degrees vs radians)  
cv2 represents images as arrays which is super helpful  
pathfinding will probably requre tuning which makes sense but maybe there is a  
way to calculate the tuning  
try not to use global variables so freely, use a config dict when possible, 
take parameters into functions, and set default values equal to the config values

# Things I still wonder
could the derivative of r(theta) be useful?
- inside of a turn would be a maximum and outside would be minimum

# Calculus things to implement in the future? (1.5)
- Detect sharpest point of a corner with parametric calculus
- look at surrounding points to determine the slope
- draw a line from that sharpest point out normal to the slope until you hit the other side of the track
- aim for the center of that line


## Possible Issues
sharpest point detected near a "dropoff" where the point used to detect slope is calculated between 2 distant points
