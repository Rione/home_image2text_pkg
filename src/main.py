import rospy
from sensor_msgs.msg import Image
from i2t import i2t_ros

def start_node():
    rospy.init_node("image2text")
    rospy.roginfo("image2text node started.")
    rospy.Subscriber("image_raw", Image, i2t_ros)
    rospy.spin()
