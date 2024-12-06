import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
import subprocess
import time

class TurtleSpawner(Node):
    def __init__(self):
        super().__init__('turtle_spawner')
        # Tạo client để gọi dịch vụ /spawn
        self.client = self.create_client(Spawn, '/spawn')
        # Đợi cho đến khi dịch vụ sẵn sàng
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Đang chờ dịch vụ /spawn...')

    def spawn_turtle(self, x, y, theta, name=None):
        # Tạo request để tạo rùa
        request = Spawn.Request()
        request.x = x
        request.y = y
        request.theta = theta
        request.name = name if name else ''  # Tùy chọn đặt tên cho rùa
        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            self.get_logger().info(f'Đã tạo rùa {future.result().name} tại vị trí: ({x}, {y})')
        else:
            self.get_logger().error('Không thể tạo rùa')

    def spawn_multiple_turtles(self, number_of_turtles):
        for i in range(number_of_turtles):
            x = (i % 5) + 1.0  # Tạo vị trí x theo lưới
            y = (i // 5) + 1.0  # Tạo vị trí y theo lưới
            theta = 0.0  # Góc quay mặc định
            name = f'turtle_{i+2}'  # Đặt tên rùa từ turtle_2 đến turtle_11
            self.spawn_turtle(x, y, theta, name)

def main(args=None):
    # Khởi động turtlesim_node trong một tiến trình mới
    subprocess.Popen(['ros2', 'run', 'turtlesim', 'turtlesim_node'])

    rclpy.init(args=args)
    turtle_spawner = TurtleSpawner()

    # Gọi hàm để tạo 10 con rùa
    turtle_spawner.spawn_multiple_turtles(10)

    turtle_spawner.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
