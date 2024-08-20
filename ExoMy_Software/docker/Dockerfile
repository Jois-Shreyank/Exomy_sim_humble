# Base image
FROM ros:humble

ENV TZ=Europe/Amsterdam
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Basic tools
RUN apt-get update && \
    apt-get install vim nano git tmux wget curl python3-pip net-tools iputils-ping zsh fonts-powerline unzip -y

# OH-MY-ZSH Installation
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)" &&\
    sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="agnoster"/' ~/.zshrc &&\
    echo "source /opt/ros/humble/setup.zsh" >> ~/.zshrc 

# Install additional ros packages
RUN sudo apt-get update && \
    sudo apt-get install ros-humble-joy -y && \
    sudo apt-get install ros-humble-async-web-server-cpp ros-humble-cv-bridge ros-humble-image-transport -y && \
    sudo apt install ros-humble-rosbridge-server -y && \
    sudo apt-get install ros-humble-image-tools -y

# Install adafruit libs
RUN sudo apt-get install python3-dev python3-rpi.gpio
RUN pip3 install adafruit-circuitpython-pca9685

# Create Ros workspace
ENV EXOMY_WS=/home/exomy/exomy_ws
RUN mkdir -p $EXOMY_WS/src
WORKDIR /root


RUN echo ". /opt/ros/$ROS_DISTRO/setup.bash" >> ~/.bashrc
## if you made changes to the code you need to comment the prebuilt temp.zip and uncomment the webserver clone to rebuild the image
## attention: this will take a long time to build or may crash the build if your're not using a powerful machine
# git clone --branch ros2 https://github.com/RobotWebTools/web_video_server 
ADD temp.zip /root/temp.zip
RUN unzip -o /root/temp.zip -d /root/

ADD entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD [ "bash" ]
