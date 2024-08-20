import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

namespace_ = 'exomy'

def generate_launch_description():
    # Get the path to the exomy.yaml parameter file
    exomy_config = os.path.join(get_package_share_directory('exomy'),'exomy.yaml')

    robot = Node(
        package='exomy',
        executable='robot_node',
        name='robot_node',
        namespace=namespace_,
        parameters=[exomy_config],
        output='screen'
    )
    joy = Node(
        package='joy',
        executable='joy_node',
        name='joy_node',
        namespace=namespace_,
        output='screen'
    )
    gamepad = Node(
        package='exomy',
        executable='gamepad_parser_node',
        name='gamepad_parser_node',
        namespace=namespace_,
        output='screen'
    )
    motors = Node(
        package='exomy',
        executable='motor_node',
        name='motor_node',
        namespace=namespace_,
        parameters=[exomy_config],
        output='screen'
    )

    rosbridge_websocket = Node(
        package='rosbridge_server',
        executable='rosbridge_websocket',
        name='rosbridge_websocket',
        output='screen'
    )

    image_tools = Node(
        package='image_tools',
        executable='cam2image',
        name='cam2image',
        remappings=[('/image', '/pi_cam/image_raw')]
    )

    web_video_server = Node(
        package='web_video_server',
        executable='web_video_server',
        name='web_video_server',
        output='screen'
    )

    return LaunchDescription([
        robot,
        gamepad,
        joy,
        motors,
        rosbridge_websocket,
        image_tools,
        web_video_server,
    ])
