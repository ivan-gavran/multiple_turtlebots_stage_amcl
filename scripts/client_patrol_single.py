#!/usr/bin/env python
import os
import rospy
import actionlib
import pdb
import argparse
import pyglet

from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose2D
from std_msgs.msg import String


class ActionExec(object):
    def __init__(self, client_topic='move_base'):
        self.client_topic = client_topic
        self.status_publisher = rospy.Publisher('patrol_status', String, queue_size=10)
        self.directions_subscriber = rospy.Subscriber('coordinator_directions', Pose2D, self.sendARobot)
        self.client = actionlib.SimpleActionClient(self.client_topic, MoveBaseAction)
        self.client.wait_for_server()
        
        rospy.logdebug('initialized action exec')
    
    def sendARobot(self, msg):
        pose = msg
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id='/map' #1 map? or should there be 1 per core?
        
        # find a better way for this transformation
        goal.target_pose.pose.position.x = pose.x
        goal.target_pose.pose.position.y = pose.y
        goal.target_pose.pose.position.z = 0.0
        goal.target_pose.pose.orientation.x = 0.0   
        goal.target_pose.pose.orientation.y = 0.0
        goal.target_pose.pose.orientation.z = 0.0
        goal.target_pose.pose.orientation.w = 1.0
        
        self.client.send_goal(goal)
        finishedOnTime = self.client.wait_for_result(rospy.Duration(60))
        state = self.client.get_state()
        #result = self.client.send_goal_and_wait(goal, rospy.Duration(60))
        # TODO
        if state == 3:
            self.status_publisher.publish("success")
        else:
            rospy.logerr("navigation failed")
            self.status_publisher.publish("failure")
            
    
def main():
    parser = argparse.ArgumentParser()
    rospy.init_node('client_patrol', anonymous=True)
    actionExecuter = ActionExec()
    rospy.spin()
    
if __name__ == '__main__':
    main()
    
