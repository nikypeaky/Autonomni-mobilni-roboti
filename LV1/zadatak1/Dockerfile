FROM ros:jazzy-ros-base

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        ros-jazzy-turtlesim \
        ros-jazzy-rosbridge-suite \
        ros-dev-tools \
        x11-apps \
    && rm -rf /var/lib/apt/lists/*

ENV DISPLAY=:0

WORKDIR /ros_ws
COPY ros_ws/src ./src
RUN . /opt/ros/jazzy/setup.sh && colcon build

# source ROS-a i workspacea u interaktivnim terminalima (docker exec ... bash)
RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc && \
    echo "source /ros_ws/install/setup.bash" >> /root/.bashrc

# Pri podizanju kontejnera automatski pokreni launch datoteku
CMD ["bash", "-c", "source /opt/ros/jazzy/setup.bash && source /ros_ws/install/setup.bash && ros2 launch turtle_path turtle_launch.xml"]
