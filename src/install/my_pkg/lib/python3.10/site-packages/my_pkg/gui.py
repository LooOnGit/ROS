import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from my_interfaces.msg import MyMsg

import json

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(MyMsg, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = MyMsg()
#        my_data = {"data1":self.i,"data2":self.i*2}
        msg.a = self.i
        msg.b =2.0*self.i
#        msg.data = json.dumps(my_data)
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: a:%d , b:%f' % (msg.a,msg.b))
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
