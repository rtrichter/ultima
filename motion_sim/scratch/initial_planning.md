# Initial plans for motion simulation

# Prototype Eveolutions
| Evolution # | Given Information    | Movement Controller  | Status        |
| ----------- | -------------------- | -------------------- | ------------- |
| 0           | Just boundaries      | give (x, y) position | WIP
| 1           | 100% accurate vision | give (x, y) position | Not Attempted |
| 2           | 100% accurate vision | tank control         | Not Attempted | 
| 3           | 100% accurate vision | PID control          | Not Attempted |
| 4           | Add Ramp             | PID control          | Not Attempted |


# The Map
## Color Codes
| Color        | Hex     | Meaning     |
| ------------ | ------- | ----------- |
| Black        | #000000 | Null space  |
| White        | #FFFFFF | Boundaries  |
| Orange       | #FF8800 | Cones       |
| Green        | #00GG00 | Ramp        |
| Ugly Green   | #87AD09 | Trees       |
| Gray         | #888888 | Posts/Signs |


# Getting information
Take a vision cone from in front of the bot  
Assume that the lidar has 100% precision for now  
Assume that cameras can perfectly detect the lines

Detect




# Pathfinding
Need to steer away from things that are close  
Steer towards things that are farther  

