from scipy.spatial.transform import Rotation as R
import math, numpy as np

q = [0.5, 0.5, 0.5, 0.5]

def euler_from_quaternion_1(q):
    r = R.from_quat(q)
    euler = r.as_euler('xyz')
    np.set_printoptions(precision=16)
    return euler
 
def euler_from_quaternion_2(q):
        # rx = msg.pose.posr.position.x
        # ry = msg.pose.posr.position.y

        x = q[0]    # msg.pose.pose.orientation.x
        y = q[1]    # msg.pose.pose.orientation.y
        z = q[2]    # msg.pose.pose.orientation.z
        w = q[3]    # msg.pose.pose.orientation.w
        euler = []

        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)

        euler.append(roll_x)
        euler.append(pitch_y)
        euler.append(yaw_z)
        return euler

print(euler_from_quaternion_1(q)[0].item())
print("-----------------------------------")
print(euler_from_quaternion_2(q)[0])

