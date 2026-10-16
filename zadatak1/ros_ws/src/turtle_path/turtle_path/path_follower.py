import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

CENTER = 5.544
AMPLITUDE = 4.0


def path_point(w):
    """Točka na putanji za parametar w."""
    x = CENTER + AMPLITUDE * math.sin(w)
    y = CENTER + AMPLITUDE * math.sin(w) * math.cos(w)
    return x, y


def path_tangent(w):
    """Derivacija putanje po w (smjer i 'brzina' putanje)."""
    dx = AMPLITUDE * math.cos(w)
    dy = AMPLITUDE * math.cos(2.0 * w)
    return dx, dy


def normalize_angle(a):
    return math.atan2(math.sin(a), math.cos(a))


class PathFollower(Node):
    def __init__(self):
        super().__init__('path_follower')

        # Parametri
        self.declare_parameter('omega_rate', 0.5)   # rad/s po putanji (1 krug ≈ 12.6 s)
        self.declare_parameter('k_pos', 3.0)        # pojačanje za pogrešku pozicije
        self.declare_parameter('k_ang', 6.0)        # pojačanje za pogrešku kuta
        self.declare_parameter('rate_hz', 50.0)

        self.omega_rate = self.get_parameter('omega_rate').value
        self.k_pos = self.get_parameter('k_pos').value
        self.k_ang = self.get_parameter('k_ang').value
        rate_hz = self.get_parameter('rate_hz').value

        self.pose = None
        self.t0 = None

        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose_sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_cb, 10)
        self.timer = self.create_timer(1.0 / rate_hz, self.control_loop)

        self.get_logger().info('Path follower pokrenut, čekam pozu kornjače...')

    def pose_cb(self, msg):
        self.pose = msg

    def control_loop(self):
        if self.pose is None:
            return

        now = self.get_clock().now()
        if self.t0 is None:
            self.t0 = now
            self.get_logger().info('Pose primljena, krećem po putanji.')

        t = (now - self.t0).nanoseconds * 1e-9
        w = (self.omega_rate * t) % (2.0 * math.pi)

        # Ciljna točka i tangencijalna brzina na putanji
        tx, ty = path_point(w)
        dx_dw, dy_dw = path_tangent(w)
        vx_ff = dx_dw * self.omega_rate
        vy_ff = dy_dw * self.omega_rate

        # Željena brzina u svijetu = feedforward + P-regulator pozicije
        vx_des = vx_ff + self.k_pos * (tx - self.pose.x)
        vy_des = vy_ff + self.k_pos * (ty - self.pose.y)

        desired_heading = math.atan2(vy_des, vx_des)
        heading_err = normalize_angle(desired_heading - self.pose.theta)

        cmd = Twist()
        cmd.linear.x = math.hypot(vx_des, vy_des) * max(0.0, math.cos(heading_err))
        cmd.angular.z = self.k_ang * heading_err
        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = PathFollower()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
