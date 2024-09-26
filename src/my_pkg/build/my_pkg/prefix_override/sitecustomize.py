import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/looubuntu/ros2_ws/src/my_pkg/install/my_pkg'
