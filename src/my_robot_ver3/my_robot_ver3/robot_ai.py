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

                #Pop
                if self.index == 10:
                    self.get_logger().info(f"Total: {sum(self.fitnessArr2)}")
                    self.pop += 1
                    self.get_logger().info(f"Pop{self.pop}")
                    fit1 = self.fitnessArr
                    self.save_matrices_to_excel(self.w1,self.w2,self.fitnessArr)
                    self.w1,self.w2 = self.selection(self.w1, self.w2, fit1, self.popSize)
                    self.w1 = self.ga(self.w1, self.popSize, self.input_size, self.hidden_size)
                    self.w2 = self.ga(self.w2, self.popSize, self.hidden_size, self.output_size)
                    self.index = 0
                self.fitness = 0
                self.start_time = time.time()
                self.w1Pre = self.w1[self.index]
                self.w2Pre = self.w2[self.index]
                self.bestFitness = 0
        j = 0
        for i, value in enumerate(laser):
            self.sensors[j] = value
            j+=1
        
        # self.sensors = laser
    
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

            #Pop
            if self.index == 10:
                self.get_logger().info(f"Total: {sum(self.fitnessArr2)}")
                self.pop += 1
                self.get_logger().info(f"Pop{self.pop}")
                self.index = 0
                fit1 = self.fitnessArr
                self.save_matrices_to_excel(self.w1,self.w2,self.fitnessArr)
                self.w1,self.w2 = self.selection(self.w1, self.w2, fit1, self.popSize)
                self.w1 = self.ga(self.w1, self.popSize, self.input_size, self.hidden_size)
                self.w2 = self.ga(self.w2, self.popSize, self.hidden_size, self.output_size)
            self.fitness = 0
            self.start_time = time.time()
            self.w1Pre = self.w1[self.index]
            self.w2Pre = self.w2[self.index]
            self.bestFitness = 0

        #Done
        if self.taget_x == self.current_x and self.taget_y == self.current_y:
            self.runCtrl(abs(0), 0)
            self.get_logger().info(f"DONE")
            self.index = 0
            self.fitnessArr[self.index] = 0 
            self.save_matrices_to_excel(self.w1,self.w2,self.fitnessArr)
            sys.exit()
        else:
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

    def selection(self, w1, w2, fitness, ngene):
        percent = []
        for i in range(len(fitness)):
            fitness[i] = 1/fitness[i]
        total = sum(fitness)
        for i in fitness:
            temp = i/total
            percent.append(temp)
        random_choice = np.random.choice(range(ngene), size=ngene, p=percent, replace=True)
        w1 = w1[random_choice,:,:]
        w2 = w2[random_choice,:,:]
        return w1, w2

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
                    crossing_point = int(pop_size/2)
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
            p[changes] = np.random.uniform(-1,1, size=len(changes[0]))
            result.append(p)
        return np.array(result)

    ################################################################################### Tổng hợp

    def ga(self, pop, ngene, input_size, hidden_size):

        pop_after_crossover = self.crossover(pop, hidden_size, input_size, ngene)
        pop_after_mutation = self.mutation(pop_after_crossover, mutation_rate = 0.1, pop_size=hidden_size, ngene=input_size)
        return pop_after_mutation
    
    def save_matrices_to_excel(self, w1, w2, fitness):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Train ROS2"
        sheet.cell(row=1, column=1, value="Hiden layer")
        sheet.cell(row=1, column=2, value="Output layer")
        sheet.cell(row=1, column=3, value="Fitness")
        row_index = 2
        for i in range(len(fitness)):
            matrix1_str = '\n'.join(['\t'.join(map(str, row)) for row in w1[i]])
            sheet.cell(row=row_index, column=1, value=matrix1_str)
            matrix2_str = '\n'.join(['\t'.join(map(str, row)) for row in w2[i]])
            sheet.cell(row=row_index, column=2, value=matrix2_str)
            sheet.cell(row=row_index, column=3, value=fitness[i])
            row_index += 2
        workbook.save(file_excel)

    def load_from_excel(self):
        workbook = openpyxl.load_workbook(file_excel)
        sheet = workbook.active
        w1 = []
        w2 = []
        fitness = []
        for row in range(2, sheet.max_row + 1):
            matrix1_str = sheet.cell(row=row, column=1).value
            matrix2_str = sheet.cell(row=row, column=2).value
            fitness_value = sheet.cell(row=row, column=3).value
            if matrix1_str:
                matrix1 = [list(map(float, line.split('\t'))) for line in matrix1_str.split('\n')]
                w1.append(matrix1)
            if matrix2_str:
                matrix2 = [list(map(float, line.split('\t'))) for line in matrix2_str.split('\n')]
                w2.append(matrix2)
            if fitness_value is not None:
                fitness.append(fitness_value)
        w1 = np.array(w1)
        w2 = np.array(w2)
        return w1, w2

def main(args=None):
    rclpy.init(args=args)
    robot_navigator = RobotNavigator()
    rclpy.spin(robot_navigator)
    robot_navigator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
