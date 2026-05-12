#!/usr/bin/env python3

import rospy
from duckietown_msgs.msg import Twist2DStamped, AprilTagDetectionArray


class TargetFollower:
    def __init__(self):
        rospy.init_node("target_follower_node")

        self.veh = rospy.get_param("~veh", "srea002453")

        self.cmd_topic = f"/{self.veh}/car_cmd_switch_node/cmd"
        self.tag_topic = f"/{self.veh}/apriltag_detector_node/detections"

        self.pub = rospy.Publisher(self.cmd_topic, Twist2DStamped, queue_size=1)

        self.sub = rospy.Subscriber(
            self.tag_topic,
            AprilTagDetectionArray,
            self.callback
        )

        self.search_speed = 1.0
        self.turn_speed = 2.0

        rospy.loginfo("Target follower started")

    def publish_cmd(self, v, omega):
        msg = Twist2DStamped()
        msg.header.stamp = rospy.Time.now()
        msg.v = v
        msg.omega = omega
        self.pub.publish(msg)

    def callback(self, msg):

        # No tags detected → search mode
        if len(msg.detections) == 0:
            rospy.loginfo("Searching for tag...")
            self.publish_cmd(0.0, self.search_speed)
            return

        # First detected tag
        detection = msg.detections[0]

        y = detection.transform.translation.y

        rospy.loginfo(f"Tag detected. y = {y}")

        # Center the tag
        if abs(y) < 0.05:
            self.publish_cmd(0.0, 0.0)

        elif y > 0:
            self.publish_cmd(0.0, -self.turn_speed)

        else:
            self.publish_cmd(0.0, self.turn_speed)


if __name__ == "__main__":
    rospy.sleep(2.0)
    node = TargetFollower()
    rospy.spin()
