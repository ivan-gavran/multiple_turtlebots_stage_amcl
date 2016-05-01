#!/usr/bin/env python
import re
import rospy
from std_msgs.msg import String
import random
from geometry_msgs.msg import Pose2D
import pdb
import argparse

class PatrolCoordinator(object):
    """def __init__(self, availableRobots=['robot_0', 'robot_1'], listOfPositions={'robot_0':[(25, 15),(23,14)],\
                                                                      'robot_1':[(24,14), (23, 15)]}):"""
#     def __init__(self, availableRobots=['robot_0', 'robot_1'], listOfPositions={'robot_0':[(0, 14),(25,15), (24,14), (23, 15), (26, 13.75)],\
#                                                                       'robot_1':[(24.5,13.25), (25, 13.25)]}):
#     
    def __init__(self, availableRobots=['robot_0', 'robot_1'], listOfPositions={'robot_0':[(1,0), (0,0)], 'robot_1':[ (1,2), (1,1)]}):
        rospy.loginfo('coordinator initialization')
        self.nextPositionIndex = {'robot_0':0, 'robot_1':0}
        self.availableRobots = availableRobots
        self.listOfPositions = {}
        self.status_subscriber={}
        self.robotPublishers = {}
        self.listOfPositions = listOfPositions
        for robotName in availableRobots:
            
            self.status_subscriber[robotName] = rospy.Subscriber(robotName+'/patrol_status', String, self.askForNextLocation)
            topic = robotName+'/coordinator_directions'
            self.robotPublishers[robotName] = rospy.Publisher(topic, Pose2D, queue_size=10, latch=True)
            
    def askForNextLocation(self, msg=String("")):
        # get the name of the node that is sending the message
        callerid = msg._connection_header['callerid']
        robotName = re.findall('/(.*)/client_node', callerid)[0]
        if msg.data == "failure":
            rospy.logerr("failure by patrolling")
        self.sendDirection(robotName)
        
    
    def sendDirection(self, robot):
        pub = self.robotPublishers[robot]
        positionIndex = self.nextPositionIndex[robot]
        position = self.listOfPositions[robot][positionIndex]
        direction = Pose2D(position[0], position[1], 0)
        pub.publish(direction)
        self.nextPositionIndex[robot] = (self.nextPositionIndex[robot] + 1) % len(self.listOfPositions[robot])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--robot_to_control", default="robot_0", help="robot's name. should be unique in order to coordinate multiple robots. default: robot_0 ")
    args, unknown = parser.parse_known_args()
    coordinator = PatrolCoordinator(availableRobots=['robot_0', 'robot_1'])
    rospy.init_node('coordinator')
    coordinator.sendDirection('robot_0')
    coordinator.sendDirection('robot_1')
    rospy.spin()

if __name__ == '__main__':
    main()
