from example_interfaces.srv import AddTwoInts

import rclpy
from rclpy.node import Node
from my_interfaces.srv import Vd

class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(Vd, 'robo', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.x + request.y
        self.get_logger().info('Incoming request\na: %f b: %f' % (request.x, request.y))

        return response


def main():
    rclpy.init()

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()