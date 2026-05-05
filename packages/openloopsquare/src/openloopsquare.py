#!/usr/bin/env python3

import rospy
from duckietown_msgs.msg import Twist2DStamped


class OpenLoopSquareNode:
    def __init__(self):
        rospy.init_node("openloopsquare_node", anonymous=False)

        self.veh = rospy.get_param("~veh", "srea002453")
        self.cmd_topic = f"/{self.veh}/car_cmd_switch_node/cmd"

        self.pub_cmd = rospy.Publisher(self.cmd_topic, Twist2DStamped, queue_size=1)

        self.forward_speed = 0.25
        self.turn_speed = 4.0

        # Tune these values for 1 metre straight and 90 degree turn
        self.forward_time = 4.0
        self.turn_time = 1.0

        rospy.on_shutdown(self.stop_robot)

        rospy.loginfo(f"OpenLoopSquareNode started for vehicle: {self.veh}")
        rospy.loginfo(f"Publishing to: {self.cmd_topic}")

    def publish_cmd(self, v, omega):
        msg = Twist2DStamped()
        msg.header.stamp = rospy.Time.now()
        msg.v = v
        msg.omega = omega
        self.pub_cmd.publish(msg)

    def stop_robot(self):
        for _ in range(5):
            self.publish_cmd(0.0, 0.0)
            rospy.sleep(0.1)

    def move_straight(self, duration):
        start = rospy.Time.now().to_sec()
        rate = rospy.Rate(10)

        while not rospy.is_shutdown() and rospy.Time.now().to_sec() - start < duration:
            self.publish_cmd(self.forward_speed, 0.0)
            rate.sleep()

        self.stop_robot()
        rospy.sleep(0.5)

    def rotate_in_place(self, duration):
        start = rospy.Time.now().to_sec()
        rate = rospy.Rate(10)

        while not rospy.is_shutdown() and rospy.Time.now().to_sec() - start < duration:
            self.publish_cmd(0.0, self.turn_speed)
            rate.sleep()

        self.stop_robot()
        rospy.sleep(0.5)

    def move_square(self):
        rospy.loginfo("Starting square motion")

        for i in range(4):
            rospy.loginfo(f"Side {i + 1}: moving straight")
            self.move_straight(self.forward_time)

            rospy.loginfo(f"Turn {i + 1}: rotating 90 degrees")
            self.rotate_in_place(self.turn_time)

        self.stop_robot()
        rospy.loginfo("Square motion complete")


if __name__ == "__main__":
    try:
        node = OpenLoopSquareNode()

        rospy.sleep(2.0)

        input("Press ENTER to start the robot square movement...")

        node.move_square()

    except rospy.ROSInterruptException:
        pass
