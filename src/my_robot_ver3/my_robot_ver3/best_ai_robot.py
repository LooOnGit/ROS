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
import time
import openpyxl
import sys
file_excel = "/home/looubuntu/ros2_ws/src/my_robot_ver3/my_robot_ver3/output.xlsx" # Tên file excel để đây cho dễ sửa

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

        self.current_x = 0.0
        self.current_y = 0.0
        self.current_theta = 0.0
        self.taget_x = 9.0
        self.taget_y = 2.0
        self.taget_theta = 0.0
        self.sensors = [1,2,3,4,5,6,7,8,9,10, 11, 12, 13, 14, 15]  # Mảng 1 chiều với 10 phần tử

        #Init neural
        self.pop = 0
        self.popSize = 10
        self.index = 0
        self.fitnessArr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.fitnessArr2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.fitness = 0

        self.input_size = 15
        self.hidden_size = 50
        self.output_size = 2

        self.w1 = np.random.uniform(-1,1,size=(self.popSize, self.input_size, self.hidden_size))
        self.w2 = np.random.uniform(-1,1,size=(self.popSize, self.hidden_size, self.output_size))

        self.w1Pre = self.w1[self.index]
        self.w2Pre = self.w2[self.index]

        self.aa = 0

        #Init pop

        self.pastFitness = -1

        self.bestFitness = 0

        self.timeStart = 0
        self.timePre = 0
        self.thetaTime = 0

        #init time
        self.timePreSys = 0
        self.timePastSys = 0 


        #PARALLELOGRAM
        self.edge = 1
        self.a = 0
        self.b = 0
        self.h = 0

        self.past = 0
        self.pre = 0
        self.get_logger().info(f"Pop{0}")

    def send_reset(self):
        return self.cli.call_async(self.req)

    def add_two_ints_callback(self, request, response):
        self.taget_x = request.x
        self.taget_y = request.y
        self.taget_theta = request.theta
        return response
    
    def read_sensor(self, msg):
        laser = np.array(msg.ranges)[:-1]
        for i, value in enumerate(laser):
            if value < 0.15:
                self.checkTouch(self.taget_x - self.current_x)
                self.send_reset()
                self.timePastSys = self.timePreSys
                self.timePreSys = time.time()
                
                #noise
                time.sleep(0.5)
                if((self.timePreSys - self.timePastSys) > 0.6):
                    self.fitnessArr[self.index] = self.bestFitness
                    self.fitnessArr2[self.index] = self.bestFitness    
                    self.get_logger().info(f"Gen{self.index}: {self.bestFitness}")   
                    self.index += 1

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def tanh(self, x):
        return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))

    def neuron(self, sensor_input, w1, w2):
        # Tính toán đầu ra lớp ẩn
        hidden_layer_input = np.dot(w1.T, sensor_input)
        hidden_layer_output = self.sigmoid(hidden_layer_input)
        
        # Tính toán đầu ra lớp ngõ ra
        output_layer_input = np.dot(w2.T,hidden_layer_output)
        output_layer_output = self.tanh(output_layer_input)
        
        return output_layer_output
    
    def checkTouch(self, x):
        self.bestFitness = self.fitness + (x * (x*700))
    
    def checkBack(self, x):
        self.bestFitness = self.fitness + (x * (x*1500))
    
    def listener_callback(self, msg):
        self.aa += 1
        #read position
        self.past_x = self.current_x
        self.past_y = self.current_y
        posRobot = msg.pose.pose.position
        oriRobot = msg.pose.pose.orientation
        self.current_x = posRobot.x
        self.current_y = posRobot.y
        # self.get_logger().info(f"{self.taget_x - self.current_x}")

        self.current_theta = self.euler_from_quaternion(oriRobot.w, oriRobot.x, oriRobot.y, oriRobot.z)
        #Neural
        self.sensors[10] = self.taget_x
        self.sensors[11] = self.taget_y
        self.sensors[12] = self.current_theta
        self.sensors[13] = self.current_x
        self.sensors[14] = self.current_y
        
        pak = self.neuron(self.sensors, self.w1Pre, self.w2Pre)
        x = pak[0]
        z = pak[1]
        # self.get_logger().info(f"{z}")

        #fitness
        if self.edge == 2:
            self.timePre = time.time()
            self.h = (self.timePre - self.timeStart)
            self.b = (self.taget_x - self.current_x) ** 2 + (self.taget_y - self.current_y) ** 2
            self.fitness += (1/2)*self.h*(self.a + self.b)
            if (self.b - self.a) > 0:
                self.bestFitness = self.fitness

            self.edge = 1
        if self.edge == 1:
            self.timeStart = time.time()
            self.edge += 1
            self.a = (self.taget_x - self.current_x) ** 2 + (self.taget_y - self.current_y) ** 2

        #check
        if (self.current_x  - self.past_x) < (-0.025):
            self.checkBack(self.taget_x - self.current_x)
            self.send_reset()
            self.timePastSys = self.timePreSys
            self.timePreSys = time.time()
            time.sleep(0.5)

            #noise
            if((self.timePreSys - self.timePastSys) > 0.6):
                self.fitnessArr[self.index] = self.bestFitness   
                self.fitnessArr2[self.index] = self.bestFitness    
                self.get_logger().info(f"Gen{self.index}: {self.bestFitness}")   
                self.index += 1

        self.runCtrl(abs(x), z)


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
