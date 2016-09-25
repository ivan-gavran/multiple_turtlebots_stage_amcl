# Running multiple robots in stage simulator with navigation stack
## Starting with two robots 
To start with two robots call `roslaunch multiple_robots_in_stage robots_in_stage.launch`. This will set two
robots in the map.
To give them a goal you can call `rostopic pub /robot_0/move_base_simple/goal geometry_msgs/PoseStamped '{header: {stamp: now, frame_id: "/map"}, pose: {position: {x: 1.0, y: 1.0, z: 0.0}, orientation: {w: 1.0}}}'` 
This would send robot_0 to impossible position: however, instead of reporting the impossible goal, global_planner would be called over and over again.
Alternatively, `python scripts/patrol_organizer` will try to send robot_0 to patrol over points (0,0) and (1,0).
