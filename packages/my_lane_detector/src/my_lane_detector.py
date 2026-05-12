#!/usr/bin/env python3

import rospy
import cv2
import numpy as np

from sensor_msgs.msg import CompressedImage


class MyLaneDetector:
    def __init__(self):
        rospy.init_node("my_lane_detector_node", anonymous=False)

        self.veh = rospy.get_param("~veh", "srea002453")
        self.image_topic = f"/{self.veh}/camera_node/image/compressed"

        rospy.Subscriber(self.image_topic, CompressedImage, self.image_callback)

        rospy.loginfo("My lane detector started")
        rospy.loginfo(f"Subscribed to: {self.image_topic}")

    def image_callback(self, msg):
        np_arr = np.frombuffer(msg.data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            return

        height, width, _ = img.shape

        # Crop bottom half of image, where lane lines usually appear
        cropped = img[int(height / 2):height, 0:width]

        # Convert to HSV for colour filtering
        hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)

        # White lane filtering
        lower_white = np.array([0, 0, 180])
        upper_white = np.array([180, 60, 255])
        white_mask = cv2.inRange(hsv, lower_white, upper_white)

        # Yellow lane filtering
        lower_yellow = np.array([20, 80, 80])
        upper_yellow = np.array([40, 255, 255])
        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Combine masks
        mask = cv2.bitwise_or(white_mask, yellow_mask)

        # Edge detection
        edges = cv2.Canny(mask, 50, 150)

        # Hough line detection
        lines = cv2.HoughLinesP(
            edges,
            rho=1,
            theta=np.pi / 180,
            threshold=30,
            minLineLength=20,
            maxLineGap=10
        )

        output = self.draw_lines(cropped, lines)

        cv2.imshow("Original Image", img)
        cv2.imshow("Cropped Image", cropped)
        cv2.imshow("Lane Mask", mask)
        cv2.imshow("Edges", edges)
        cv2.imshow("Detected Lines", output)
        cv2.waitKey(1)

    def draw_lines(self, image, lines):
        output = np.copy(image)

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(output, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.circle(output, (x1, y1), 3, (0, 255, 0), -1)
                cv2.circle(output, (x2, y2), 3, (0, 0, 255), -1)

        return output

    def clean_shutdown(self):
        cv2.destroyAllWindows()


if __name__ == "__main__":
    detector = MyLaneDetector()
    rospy.on_shutdown(detector.clean_shutdown)
    rospy.spin()
