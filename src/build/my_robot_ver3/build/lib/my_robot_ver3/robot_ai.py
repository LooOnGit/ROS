import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import numpy as np
from my_interfaces.srv import Vd
from nav_msgs.msg import Odometry
import math
from std_srvs.srv import Empty
from gazebo_msgs.srv import SetEntityState
from sensor_msgs.msg import LaserScan

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

        self.subscription2 = self.create_subscription(
            LaserScan,
            '/laser_scan',
            self.read_sensor,
            10)
        self.subscription2  # prevent unused variable warning

        self.srv = self.create_service(Vd, 'roboctrl', self.add_two_ints_callback)

        self.cli = self.create_client(Empty, '/reset_simulation')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = Empty.Request()

        self.cli = self.create_client(Empty, '/reset_world')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service /reset_world not available, waiting again...')
        self.req2 = Empty.Request()

        self.current_x = 0.0
        self.current_y = 0.0
        self.current_theta = 0.0
        self.taget_x = 0.0
        self.taget_y = 0.0
        self.taget_theta = 0.0

        #Init neural
        self.w1 = 0
        self.b1 = 0
        self.w2 = 0
        self.b2 = 0

        self.input_size = 10
        self.hidden_size = 6
        self.output_size = 2

    def send_reset(self):
        return self.cli.call_async(self.req)
    
    def send_reset_world(self):
        return self.cli.call_async(self.req2)

    def add_two_ints_callback(self, request, response):
        self.taget_x = request.x
        self.taget_y = request.y
        self.taget_theta = request.theta
        return response
    
    def read_sensor(self, msg):
        laser = np.array(msg.ranges)
        # self.get_logger().info(f"{laser[0]}")
        return np.array(msg.ranges)
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def neuron(sself, sensor_input, w1, b1, w2, b2):
        # Tính toán đầu ra lớp ẩn
        hidden_layer_input = np.dot(sensor_input, w1) + b1
        hidden_layer_output = self.sigmoid(hidden_layer_input)
        
        # Tính toán đầu ra lớp ngõ ra
        output_layer_input = np.dot(hidden_layer_output, w2) + b2
        output_layer_output = self.sigmoid(output_layer_input)
        
        return output_layer_output

    def listener_callback(self, msg):
        #read position
        # posRobot = msg.pose.pose.position
        # oriRobot = msg.pose.pose.orientation
        # self.current_x = posRobot.x
        # self.current_y = posRobot.y
        # self.current_theta = self.euler_from_quaternion(oriRobot.w, oriRobot.x, oriRobot.y, oriRobot.z)

        #Neural
        # NN.neuron(self.read_sensor(msg), )

        self.runCtrl()
        # self.get_logger().info(f"x: {x}, y: {y} z = {z}")


    def euler_from_quaternion(self, w, x, y, z):
        t3 = +2.0 * (w*y - z *x)
        t4 = +1 - 2.0 * (y*y + z*z)
        yaw_z = math.atan2(t3, t4)
        return yaw_z


    def runCtrl(self, x, z):
        msg = Twist()

        msg.linear.x = float(x)
        # msg.linear.y = float(V[1])
        msg.angular.z = float(z)

        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    robot_navigator = RobotNavigator()
    rclpy.spin(robot_navigator)
    robot_navigator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
