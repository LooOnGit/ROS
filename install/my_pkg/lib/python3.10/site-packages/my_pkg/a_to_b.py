import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from math import atan2, sqrt, pi
from my_interfaces.srv import Vd

class RobotNavigator(Node):

    def __init__(self):
        super().__init__('robot_navigator')

        # Tạo publisher để gửi tin nhắn Twist
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        # Tạo subscriber để nhận tin nhắn Pose
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.listener_callback,
            10)
        self.subscription  # Để tránh cảnh báo biến không sử dụng

        self.srv = self.create_service(Vd, 'roboctrl', self.add_two_ints_callback)

        # Tọa độ điểm mục tiêu (B)
        self.target_x = 5.0
        self.target_y = 5.0

        # Khởi tạo giá trị vị trí và góc hiện tại
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_theta = 0.0

        # Ngưỡng khoảng cách và góc để dừng lại
        self.distance_threshold = 0.1
        self.angle_threshold = 0.1

        # Thiết lập timer để điều khiển robot liên tục
        self.timer = self.create_timer(0.1, self.navigate)

    def listener_callback(self, msg):
        self.current_x = msg.x
        self.current_y = msg.y
        self.current_theta = msg.theta

    def navigate(self):
        dx = self.target_x - self.current_x
        dy = self.target_y - self.current_y
        distance = sqrt(dx**2 + dy**2)
        target_angle = atan2(dy, dx)
        angle_diff = self.normalize_angle(target_angle - self.current_theta)

        msg = Twist()

        if distance > self.distance_threshold:
            if abs(angle_diff) > self.angle_threshold:
                msg.angular.z = 0.5 if angle_diff > 0 else -0.5
            else:
                msg.linear.x = 1.0
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        self.publisher_.publish(msg)

    def normalize_angle(self, angle):
        # Hàm để đưa góc về khoảng -pi đến pi
        while angle > pi:
            angle -= 2 * pi
        while angle < -pi:
            angle += 2 * pi
        return angle
    
    def add_two_ints_callback(self, request, response):
        self.target_x = request.x
        self.target_y = request.y
        self.get_logger().info('Incoming request\na: %f b: %f' % (request.x, request.y))

        return response


def main(args=None):
    rclpy.init(args=args)
    robot_navigator = RobotNavigator()
    rclpy.spin(robot_navigator)
    robot_navigator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
