#!/usr/bin/env python
from exomy_msgs.msg import RoverCommand, MotorCommands
import rclpy
from rclpy.node import Node
from .rover import Rover


class RobotNode(Node):
    def __init__(self):
        self.node_name = 'robot_node'
        super().__init__(self.node_name)

        self.joy_sub = self.create_subscription(
            RoverCommand,
            'rover_command',
            self.joy_callback,
            10)

        self.robot_pub = self.create_publisher(
            MotorCommands,
            'motor_commands',
            1)
        self.robot = Rover()

        self.get_logger().info('\t{} STARTED.'.format(self.node_name.upper()))

    def joy_callback(self, msg):
        cmds = MotorCommands()

        if msg.force_stop:
            # Decrease vel linearly until 0
            vel = msg.vel

            while vel > 0:
                cmds.motor_angles = self.robot.joystickToSteeringAngle(vel, msg.steering)
                cmds.motor_speeds = self.robot.joystickToVelocity(vel, msg.steering)
                self.robot_pub.publish(cmds)
                vel -= 0.1  # Adjust the decrement value as needed

            cmds.motor_speeds = [0, 0, 0, 0, 0, 0]
            self.robot_pub.publish(cmds)
        else:
            self.robot.setLocomotionMode(msg.locomotion_mode)
            cmds.motor_angles = self.robot.joystickToSteeringAngle(msg.vel, msg.steering)
            cmds.motor_speeds = self.robot.joystickToVelocity(msg.vel, msg.steering)
            self.robot_pub.publish(cmds)

def main(args=None):
    rclpy.init(args=args)

    try:
        robot_node = RobotNode()
        try:
            rclpy.spin(robot_node)
        finally:
            robot_node.destroy_node()
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()
