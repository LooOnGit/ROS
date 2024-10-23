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
        self.sensors = np.zeros(10)  # Mảng 1 chiều với 10 phần tử

        #Init neural
        self.pop = 10
        self.index = 0
        self.fitnessArr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.fitness = 0

        self.input_size = 10
        self.hidden_size = 6
        self.output_size = 2


        self.w1 = np.random.uniform(-2,2,size=(self.pop, self.input_size, self.hidden_size))
        self.w2 = np.random.uniform(-2,2,size=(self.pop, self.hidden_size, self.output_size))
        self.b2 = np.random.randn(self.output_size)
        self.b1 = np.random.randn(self.hidden_size)

        self.w1Pre = self.w1[self.index]
        self.w2Pre = self.w2[self.index]

        #Init pop

        self.pastFitness = -1

        self.bestFitness = 0

        self.start_time = time.time()
        self.thetaTime = 0

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
            if value < 0.3:
                self.bestFitness = self.bestFitness - 999
                self.send_reset()
                time.sleep(0.1)
                self.get_logger().info(f"Gen{self.index}: {self.bestFitness}")
                self.fitnessArr[self.index] = self.bestFitness
                self.get_logger().info(f"{self.fitnessArr}")
                self.index += 1
                if self.index == 10:
                    self.index = 0
                    self.w1 = self.ga(self.w1, self.fitnessArr, self.pop, self.input_size, self.hidden_size)
                    self.w2 = self.ga(self.w2, self.fitnessArr, self.pop, self.hidden_size, self.output_size)
                self.fitness = 0
                self.start_time = time.time()
                self.w1Pre = self.w1[self.index]
                self.w2Pre = self.w2[self.index]
                self.bestFitness = 0
        
        # self.get_logger().info(f"{laser[0]}")
        self.sensors = laser
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def neuron(self, sensor_input, w1, b1, w2, b2):
        # Tính toán đầu ra lớp ẩn
        hidden_layer_input = np.dot(sensor_input, w1) + b1
        hidden_layer_output = self.sigmoid(hidden_layer_input)
        
        # Tính toán đầu ra lớp ngõ ra
        output_layer_input = np.dot(hidden_layer_output, w2) + b2
        output_layer_output = self.sigmoid(output_layer_input)
        
        return output_layer_output
    
    def listener_callback(self, msg):
        #read position
        self.past_x = self.current_x
        self.past_y = self.current_y
        posRobot = msg.pose.pose.position
        oriRobot = msg.pose.pose.orientation
        self.current_x = posRobot.x
        self.current_y = posRobot.y
        self.current_theta = self.euler_from_quaternion(oriRobot.w, oriRobot.x, oriRobot.y, oriRobot.z)
        #Neural
        pak = self.neuron(self.sensors, self.w1Pre, self.b1, self.w2Pre, self.b2)
        x = pak[0]*1.5
        z = pak[1]*1.5

        #fitness


        # Mục tiêu là khoảng cách từ vị trí hiện tại đến tọa độ mục tiêu (taget_x, taget_y)
        distance_to_goal = math.sqrt((self.taget_x - self.current_x) ** 2 + (self.taget_y - self.current_y) ** 2)

        # Kiểm tra nếu có vật cản phía trước
        obstacle_distance = min(self.sensors)

        # Trọng số cho khoảng cách tới mục tiêu, tránh vật cản, và thời gian
        alpha = 15 # Trọng số cho mục tiêu
        beta =  5  # Trọng số cho tránh vật cản
        gamma = 2  # Trọng số cho thời gian, giá trị này bạn có thể điều chỉnh

        self.thetaTime = time.time() - self.start_time
        # Fitness càng cao khi khoảng cách càng nhỏ và thời gian ít hơn
        self.fitness= (alpha / distance_to_goal) + (beta * obstacle_distance) + (gamma / self.thetaTime)

        if self.fitness > self.bestFitness:
            self.bestFitness = self.fitness

        self.runCtrl(x, z)
        # self.get_logger().info(f"fitness: {self.fitness}")

        if(self.thetaTime) > 10:
            if self.fitness < 10:
                self.bestFitness = self.bestFitness - 9999
                self.send_reset()
                time.sleep(0.1)
                self.get_logger().info(f"Gen{self.index}: {self.bestFitness}")
                self.fitnessArr[self.index] = self.bestFitness
                self.get_logger().info(f"{self.fitnessArr}")
                self.index += 1
                if self.index == 10:
                    self.index = 0
                    self.w1 = self.ga(self.w1, self.fitnessArr, self.pop, self.input_size, self.hidden_size)
                    self.w2 = self.ga(self.w2, self.fitnessArr, self.pop, self.hidden_size, self.output_size)
                self.fitness = 0
                self.start_time = time.time()
                self.w1Pre = self.w1[self.index]
                self.w2Pre = self.w2[self.index]
                self.bestFitness = 0


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

    def selection(self, pop, fitness, ngene):
        percent = []
        for i in range(len(fitness)):
            fitness[i] = fitness[i] + 10000
        total = sum(fitness)
        for i in fitness:
            temp = i/total
            percent.append(temp)
        random_choice = np.random.choice(range(ngene), size=ngene, p=percent, replace=False)
        result = pop[random_choice,:,:]
        return np.array(result)

    ################################################################################### Code lai ghép của nhóm

    def crossover(self, pop, pop_size, input_size, ngene):
        result = []
        if pop_size == 2:
            pop_size += 1
        for i in range(ngene):
            if i %2 == 0:
                p1 = pop[i]
                p2 = pop[i+1]
                f1 = []
                f2 = []
                for _ in range(input_size):
                    crossing_point = np.random.randint(1, pop_size-1)
                    f1.append(np.concatenate((p1[_][:crossing_point], p2[_][crossing_point:])))
                    f2.append(np.concatenate((p2[_][:crossing_point], p1[_][crossing_point:])))
                f1 = np.array(f1)
                result.append(f1)
                f2 = np.array(f2)
                result.append(f2)
        return np.array(result)

    ################################################################################### Code đột biến của nhóm

    def mutation(self, pop, mutation_rate, pop_size, ngene):
        result = []
        for p in pop:
            matrix = np.random.rand(ngene, pop_size)
            changes = np.where(matrix < mutation_rate)
            p[changes] = np.random.uniform(-2,2, size=len(changes[0]))
            result.append(p)
        return np.array(result)

    ################################################################################### Tổng hợp

    def ga(self, pop, fitness, ngene, input_size, hidden_size):
        pop_after_selection = self.selection(pop, fitness, ngene)
        pop_after_crossover = self.crossover(pop_after_selection, hidden_size, input_size, ngene)
        pop_after_mutation = self.mutation(pop_after_crossover, mutation_rate = 0.1, pop_size=hidden_size, ngene=input_size)
        return pop_after_mutation

def main(args=None):
    rclpy.init(args=args)
    robot_navigator = RobotNavigator()
    rclpy.spin(robot_navigator)
    robot_navigator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
