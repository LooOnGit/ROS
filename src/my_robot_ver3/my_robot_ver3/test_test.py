import numpy as np
import time

class TestDerivative:
    def __init__(self, end_point):
        self.end_point = np.array(end_point)
        
        self.prev_error_x_squared = 0
        self.prev_error_y_squared = 0
        self.integral_error_x_squared = 0
        self.integral_error_y_squared = 0
        self.prev_time = time.time()

    def update_position(self, rx, ry):
        current_time = time.time()
        delta_time = current_time - self.prev_time
        
        if delta_time > 0:
            error_x = rx - self.end_point[0]
            error_y = ry - self.end_point[1]
            
            error_x_squared = error_x ** 2
            error_y_squared = error_y ** 2
            
            # Đạo hàm của sai số bình phương theo thời gian
            derivative_error_x_squared = (error_x_squared - self.prev_error_x_squared) / delta_time
            derivative_error_y_squared = (error_y_squared - self.prev_error_y_squared) / delta_time
            
            # Tích phân sai số bình phương
            self.integral_error_x_squared += error_x_squared * delta_time
            self.integral_error_y_squared += error_y_squared * delta_time
            
            self.prev_error_x_squared = error_x_squared
            self.prev_error_y_squared = error_y_squared
            
            self.prev_time = current_time

            total_error = np.sqrt(error_x_squared + error_y_squared)

            print(f"rx: {rx:.2f}, ry: {ry:.2f}")
            print(f"Error X^2: {error_x_squared:.4f}, Derivative X^2: {derivative_error_x_squared:.4f}")
            print(f"Error Y^2: {error_y_squared:.4f}, Derivative Y^2: {derivative_error_y_squared:.4f}")
            print(f"Integral X^2: {self.integral_error_x_squared:.4f}, Integral Y^2: {self.integral_error_y_squared:.4f}")
            print(f"Total Error: {total_error:.4f}")
            print("\n")

def simulate_movement():
    test = TestDerivative(end_point=[3, 1])

    positions = [
        (2.5, 0.5),
        (2.7, 0.8),
        (2.9, 0.95),
        (3.1, 1.05),
        (3.0, 1.0),  # Điểm đích
        (3.2, 1.1),  # Vượt qua điểm đích
        (3.3, 1.15)
    ]

    for pos in positions:
        rx, ry = pos
        test.update_position(rx, ry)
        time.sleep(0.5) 

if __name__ == "__main__":
    simulate_movement()
