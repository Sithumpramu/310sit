#!/usr/bin/env python3

# Import Dependencies
import rospy 
from geometry_msgs.msg import Twist 
import time 

def move_turtle_square(): 
    rospy.init_node('turtlesim_square_node', anonymous=True)
    
    # Init publisher
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10) 
    rospy.loginfo("Turtles are great at drawing squares!")

    rospy.sleep(1)  # allow publisher to connect

    ########## FIXED CODE ##########
    while not rospy.is_shutdown():

        for _ in range(4):

            # Move forward
            cmd_vel_msg = Twist()
            cmd_vel_msg.linear.x = 2.0
            cmd_vel_msg.angular.z = 0.0
            velocity_publisher.publish(cmd_vel_msg)
            time.sleep(2)

            # Stop
            velocity_publisher.publish(Twist())
            time.sleep(0.5)

            # Turn 90 degrees
            cmd_vel_msg = Twist()
            cmd_vel_msg.linear.x = 0.0
            cmd_vel_msg.angular.z = 1.57   # ~90 degrees
            velocity_publisher.publish(cmd_vel_msg)
            time.sleep(1)

            # Stop
            velocity_publisher.publish(Twist())
            time.sleep(0.5)

    ###########################################

if __name__ == '__main__': 

    try: 
        move_turtle_square() 
    except rospy.ROSInterruptException: 
        pass
