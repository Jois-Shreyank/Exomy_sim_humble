# ExoMy - Software Repository Neusta France Version
This repository contains the software to run Exomy. The [wiki](https://github.com/esa-prl/ExoMy/wiki) explains you how to use the original software. This repository is a fork of the original software repository. The original software repository can be found [here](https://github.com/0xD0M1M0/ExoMy_Software).

<div style="text-align: center;">
    <img src="exomy_neusta_france.jpg" width="40%" height="40%" alt="ExoMy Neusta France Version">
</div>

## Installation
To configure the software on your Raspberry Pi, follow the instructions in the [wiki](https://github.com/0xD0M1M0/ExoMy/wiki/Software-Instructions "Software Instructions") of the original repository until the step Get Source Code where you will need to clone this repository instead of the original one.

### Get Source Code

To get the source code from GitHub, follow these steps:

1. Open your terminal and navigate to your home folder by running the command `cd`.

2. Clone the repository by running the command:
    ```
    https://github.com/SENEAss/ExoMy_Software.git ~/ExoMy_Software
    ```

3. To verify that the cloning was successful, run the command `ls` in your terminal. You should see a folder called `ExoMy_Software` listed.

### Run Docker Containers

To run the Docker containers, the steps are the same as in the `Software Instructions` of the original repository. For example to run the `exomy` container as auto-starting, run the following command:

```
sh ~/ExoMy_Software/docker/run_exomy.sh -a
```

Once running, you should be able to see the motors moving to demonstrate that the software is working correctly and able to connect to it via the application android or the web interface.


## Changes
The main changes in this repository are:
- The suppression of the `exomy` original web server and interface.
- The addition of a rosbridge server to communicate with the ExoMy robot.
- The addition of video streaming server to stream the video from the Raspberry Pi camera to the web interface.
- Update of the adafuit motor hat library to the latest version.
- Update of motors configuration scripts to use the new library version.
- Update the launch scripts to use the new rosbridge server and video streaming server.
- Added a force stop function to the exomy package to stop the motors in case of emergency.
