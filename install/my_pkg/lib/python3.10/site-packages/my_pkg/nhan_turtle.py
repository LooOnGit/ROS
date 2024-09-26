import rclpy
from rclpy.node import Node

from std_msgs.msg import String

from my_interfaces.msg import MyMsg

import json

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            MyMsg,
            'turtle1/pose',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
#        data = json.loads(msg.data)
#      data1 = int(data["data1"])
#       data2 = int(data["data2"])
#        self.get_logger().info('data1: %d, data2: %d' % (data1, data2))
        self.get_logger().info('data1: %d, data2: %f' % (msg.a, msg.b))


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
