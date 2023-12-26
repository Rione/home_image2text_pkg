#!/usr/bin/python3

import rospy
from image2text import i2t
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from std_msgs.msg import String

class i2t_node:
    def __init__(self):
        self.i2t = i2t()
        self.sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.callback)
        self.pub = rospy.Publisher("/i2t_text", String, queue_size=1)

    def callback(self, msg):
        bridge = CvBridge()
        image_raw = bridge.imgmsg_to_cv2(msg, "bgr8")
        text = self.i2t.image2text(image_raw)
        self.pub.publish(text)

if __name__ == "__main__":
    rospy.init_node("i2t_node")
    i2t_node()
    rospy.spin()

