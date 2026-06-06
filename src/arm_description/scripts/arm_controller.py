#!/usr/bin/env python3
"""
4-DOF Arm Controller — Interactive joint angle setter via Position Controllers.
Usage: ros2 run arm_description arm_controller.py
"""

import math
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

JOINT_LIMITS = [  # (min_deg, max_deg)
    (-180, 180),  # joint1 — base yaw
    (-90, 90),  # joint2 — shoulder
    (-90, 90),  # joint3 — elbow
    (-90, 90),  # joint4 — wrist
]


class ArmController(Node):
    def __init__(self):
        super().__init__("arm_controller_node")
        # Match the JointGroupPositionController interface
        self.pub = self.create_publisher(
            Float64MultiArray, "/arm_controller/commands", 10
        )
        self.get_logger().info("Arm Position Controller ready!")

    def send_angles(self, angles_deg: list):
        """Send a array of 4 joint angles (degrees converted to radians) directly."""
        angles_rad = [math.radians(a) for a in angles_deg]

        msg = Float64MultiArray()
        msg.data = angles_rad

        self.pub.publish(msg)
        self.get_logger().info(
            f"Sent positions: {[round(a, 2) for a in angles_deg]} deg "
            f"→ {[round(a, 4) for a in angles_rad]} rad"
        )

    def validate(self, angles_deg: list) -> bool:
        """Check all angles are within joint limits."""
        for i, (a, (lo, hi)) in enumerate(zip(angles_deg, JOINT_LIMITS)):
            if not (lo <= a <= hi):
                print(f" ERROR: joint{i+1} = {a}° is outside [{lo}°, {hi}°]")
                return False
        return True


def main():
    rclpy.init()
    node = ArmController()

    print()
    print("==================================================")
    print("    4-DOF Arm Interactive Position Controller      ")
    print("==================================================")
    print(" Enter 4 angles in DEGREES separated by commas")
    print(" Example: 0, 45, -30, 20")
    print(" Joint limits:")
    print("   joint1 (base yaw)   : -180 to 180 deg")
    print("   joint2 (shoulder)   : -90 to 90 deg")
    print("   joint3 (elbow)      : -90 to 90 deg")
    print("   joint4 (wrist)      : -90 to 90 deg")
    print(" Type 'home' -> go to 0,0,0,0")
    print(" Type 'quit' -> exit")
    print("==================================================")
    print()

    try:
        while rclpy.ok():
            raw = input("Angles (j1,j2,j3,j4) in deg > ").strip()
            if raw.lower() in ("quit", "q", "exit"):
                break
            if raw.lower() == "home":
                node.send_angles([0.0, 0.0, 0.0, 0.0])
                continue
            try:
                parts = [float(x.strip()) for x in raw.split(",")]
            except ValueError:
                print(" Bad input — enter 4 numbers separated by commas.")
                continue
            if len(parts) != 4:
                print(f" Need exactly 4 values, got {len(parts)}")
                continue
            if node.validate(parts):
                node.send_angles(parts)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
