> NOTE: This is the `ros-humble` implementation. It contains how the `smc_l298n_ros_plugin` is used with a `differntial drive robot`.
>
> It also shows how to set up `ros2-control`, `ros2-controllers`, and the `controller-manager` to work with the `smc_l298n_pid_driver module` (check the `config` and `launch` folder).  

## How to quickly setup the `smc_l298n_pid_driver module` with the `smc_diff_bot` using the `smc_l298n_ros_plugin` pkg
- ensure the **`smc_l298n_pid_driver`** module (with the motors connected and fully set up for velocity PID) is connected to the microcomputer or PC via USB.

- ensure you have successfully installed and built the [**`smc_l298n_ros_plugin`**](https://github.com/samuko-things-company/smc_l298n_ros_plugin/tree/humble) package in your ros workspace and also sourced it.

- In the `src/` folder of your `ros workspace`, clone the repo
  (or you can download and add it manually to the `src/` folder)
  > *NOTE: if you download it, extract it and change the folder name to `smc_diff_bot` before moving it to the `src/` folder*
  ```shell
  git clone -b humble https://github.com/samuko-things-company/smc_diff_bot.git
  ```

- from the `src/` folder, cd into the root directory of your `ros workspace` and run rosdep to install all necessary ros dependencies
  ```shell
  cd ../
  rosdep install --from-paths src --ignore-src -r -y
  ```

- check the serial port the driver is connected to:
  > The best way to select the right serial port (if you are using multiple serial device) is to select by path
  ```shell
  ls /dev/serial/by-path
  ```
  > you should see a value (if the driver is connected and seen by the computer), your serial port would be -> /dev/serial/by-path/[value]. for more info visit this tutorial from [ArticulatedRobotics](https://www.youtube.com/watch?v=eJZXRncGaGM&list=PLunhqkrRNRhYAffV8JDiFOatQXuU-NnxT&index=8)

  - OR you can also try this:
  ```shell
  ls /dev/ttyU*
  ```
  > you should see /dev/ttyUSB0 or /dev/ttyUSB1 and so on

- once you have gotten the **port**, update the **port** parameter in the `ros2_control` tag in the `robot_urdf.xacro` file with the discovered port in the previous step

- build the packages with colcon (in your `ros workspace` root folder):
  ```shell
  colcon build --packages-select smc_diff_bot --symlink-install
  ```


## Test the smc_diff_bot (with the smc_l298n_pid_driver connected)
- ensure you source your `ros workspace` in the terminal

- view the robot in rviz with this command
  ```shell
  ros2 launch smc_diff_bot robot_test_view.launch.py
  ```

- start the `smc_diff_bot` with the `smc_l298n_ros_plugin` (using the controller manager package)
  ```shell
  ros2 launch smc_diff_bot robot_server_control.launch.py
  ```

- while the `robot_server_control` is running, you can view the robot with odometery data by runing the following in a new terminal
  ```shell
  ros2 launch smc_diff_bot robot_client_view.launch.py
  ```

- you can now control the motors via a teleop package and notice how the robot changes position in rviz (as in the video above)
> you can also use my [arrow_key_teleop_package](https://github.com/samuko-things/arrow_key_teleop_drive)

> **feel free to use, copy and edit the smc_diff_drive package codes and launch files in your preferred project**
