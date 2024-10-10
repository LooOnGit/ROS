import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import numpy as np
from my_interfaces.srv import Vd
from nav_msgs.msg import Odometry

class RobotNavigator(Node):

    def __init__(self):
        super().__init__('robot_navigator')

        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

        self.subscription = self.create_subscription(
            Odometry,
            '/wheel/odometry',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.srv = self.create_service(Vd, 'roboctrl', self.add_two_ints_callback)

        self.current_x = 0.0
        self.current_y = 0.0
        self.current_theta = 0.0
        self.taget_x = 0.0
        self.taget_y = 0.0
        self.taget_theta = 0.0

    def add_two_ints_callback(self, request, response):
        self.taget_x = request.x
        self.taget_y = request.y
        self.taget_theta = request.theta
        return response

    def listener_callback(self, msg):
        posRobot = msg.pose.pose.position
        oriRobot = msg.pose.pose.orientation
        self.current_x = posRobot.x
        self.current_y = posRobot.y
        self.current_theta = oriRobot.z
        self.runCtrl()
        # self.get_logger().info(f"x: {x}, y: {y} z = {z}")

    def runCtrl(self):
        self.x_e = self.current_x - self.taget_x
        self.y_e = self.current_y - self.taget_y 
        self.theta_e = self.current_theta - self.taget_theta

        R = np.array([[np.cos(self.current_theta ), np.sin(self.current_theta ), 0],
                      [-np.sin(self.current_theta ), np.cos(self.current_theta ), 0],
                      [0, 0, 1]])
        G = -np.array([[self.x_e], [self.y_e], [self.theta_e]])

        V = 1 * R @ G

        msg = Twist()

        msg.linear.x = float(V[0])
        msg.linear.y = float(V[1])
        msg.angular.z = float(V[2])

        self.publisher_.publish(msg)

        self.get_logger().info('Incoming request\nax: %f y: %f theta: %f' % (V[0], V[1], V[2]))


def main(args=None):
    rclpy.init(args=args)
    robot_navigator = RobotNavigator()
    rclpy.spin(robot_navigator)
    robot_navigator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
