# Base image
FROM osrf/ros:humble-desktop

ENV TZ=Europe/Amsterdam
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Update and Upgrade the docker image
RUN apt-get update && \
    apt-get upgrade -y

# Basic tools
RUN apt-get update && \
    apt-get install vim nano git tmux wget curl python3-pip net-tools iputils-ping zsh psmisc -y

# OH-MY-ZSH Installation
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)" &&\
    sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="avit"/' ~/.zshrc &&\
    echo "source /opt/ros/humble/setup.zsh" >> ~/.zshrc 

# Install additional ros packages
RUN sudo apt-get update && \
    sudo apt-get install \
    ros-humble-joint-state-publisher \
    ros-humble-joy \
    ros-humble-gazebo-ros \
    ros-humble-gazebo-plugins \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-async-web-server-cpp\
    ros-humble-cv-bridge\
    ros-humble-image-transport \
    ros-humble-image-tools \
    ros-humble-rosbridge-server \
    ros-humble-rqt-tf-tree \
    ros-humble-tf2-tools \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-robot-localization -y

# Install python package for PWM board
RUN pip3 install adafruit-circuitpython-pca9685


# Install packages for web application
RUN curl -sL https://deb.nodesource.com/setup_18.x | sudo bash -
RUN sudo apt-get update && \
    sudo apt-get install nodejs -y

ENV NPM_CONFIG_PREFIX=/home/exomy/.npm-global
ENV PATH=$PATH:/home/exomy/.npm-global/bin
RUN npm install http-server -g

# Create Ros workspace
ENV EXOMY_WS=/home/exomy/exomy_ws
RUN mkdir -p $EXOMY_WS/src
WORKDIR /home/exomy/exomy_ws

# Clone and install the web_video_server package
RUN git clone -b ros2 https://github.com/RobotWebTools/web_video_server.git src/web_video_server

RUN echo ". /opt/ros/$ROS_DISTRO/setup.zsh" >> ~/.zshrc
RUN echo ". /usr/share/gazebo/setup.sh" >> ~/.zshrc

#ADD entrypoint.sh /entrypoint.sh
#ENTRYPOINT ["/entrypoint.sh"]
CMD [ "zsh" ]
