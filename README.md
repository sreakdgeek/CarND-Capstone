### Team Happy Feat

- Harshit Sharma	hrsht.sarma@gmail.com	@harshit_sharma (Team Lead)
- Liyou Zhou	leothemagnificent@gmail.com	@liyouzhou
- Mav S	maverick.udacity@gmail.com	@maverick
- Srikanth Vidapanakal	srikanth.vid@gmail.com					
- Paul Lech	paullech@me.com

This is the project repo for the final project of the Udacity Self-Driving Car Nanodegree: Programming a Real Self-Driving Car. For more information about the project, see the project introduction [here](https://classroom.udacity.com/nanodegrees/nd013/parts/6047fe34-d93c-4f50-8336-b70ef10cb4b2/modules/e1a23b06-329a-4684-a717-ad476f0d8dff/lessons/462c933d-9f24-42d3-8bdc-a08a5fc866e4/concepts/5ab4b122-83e6-436d-850f-9f4d26627fd9).

[//]: # (Image References) 
[image1]: ./readme_imgs/capstone_big_picture.PNG
[image2]: ./readme_imgs/way_point_node.PNG
[image3]: ./readme_imgs/traffic_light_node.PNG
[image4]: ./readme_imgs/dbw_node.PNG
[image5]: ./readme_imgs/sim_out_green.jpg
[image6]: ./readme_imgs/sim_out_yellow.jpg
[image7]: ./readme_imgs/parking_lot_red.jpg
[image8]: ./readme_imgs/parking_lot_green.jpg

# Introduction

This project involves integrating components required to navigate a car in a simulator as well as a real car in parking lot area using perception, planning and control components.

## System Architecture

Below is high-level architecture diagram showing components and the interactions:

![alt text][image1]

ROS (Robot operating system) is used to design and develop the components of this project. ROS uses a pub-sub model architecture
to design the interactions and information flow between the components. Key components of any self driving car are:

1. Perception
2. Planning 
3. Control

A self-driving car needs to perceive the world around it and recognize obstacles, traffic lights, plan its path and control the
trajectory, speed and acceleration with which the car is moving. As part of this project, Waypoint loader and Waypoint Updater components are developed to plan the trajectory or way points along which the car will navigate. Based on the information received from the perception module, DBW (Drive By Wire) Node decides the velocity and the acceleration with which car needs to move. These modules are discussed in detail in below sections.
## Components

### Waypoint Updater

![alt text][image2]

The waypoint_updater node is used to process the track waypoints from the track and provide the next waypoints for the vehicle to follow and adjust the speed depending on the traffic lights.

With the guide of the classroom walkthrough we subscribe to /current_pose, /base_waypoints, and /traffic_waypoint. The basic function of these nodes are as follows:

current_pose: Receives the current position of the vehicle.

base_waypoints: Waypoints for the entire track.

traffic_waypoint: Receives index from base_waypoints then waypoint updater uses this to calculate the distance between the vehicle and traffic light.

## DBW Node

![alt text][image4]

## Traffic light detector

![alt text][image3]

Traffic light detector component is responsible for detecting if the upcoming waypoint is red signal and if so publish the nearest waypoint to the DBW node. From the set of waypoints that are ahead of the car, traffic light detector detects the color of the closest traffic signal ahead. It publishes the index of the red traffic light signal to the DBW node, which based on the distance to the waypoint decides on the velocity with which the car needs to move. Nearest neighbor approach is used to identify the
closest waypoint to the car position and a classifier or object detector is used to localize and classify the color of the signal.

### Traffic Light localization and classification

Deep neural networks are really effective at classifying and localizing different types of objects such as traffic lights, vehicles, etc. We have explored different models such as using simple classifiers that only looks at pixel colors around approximate portion of traffic signals as well as using object detection models such as Mobilenet SSD, SSD Inception v2 etc. We have experimented and trained our models using Bosch Traffic Light data set, simulator traffic sign data and Udacity parking lot data. Eventually we created two models to detect and classify in simulator and parking lot. Below are the results:

### Simulation Images

![alt text][image5]
![alt text][image6]

### Parking lot Images

![alt text][image7]
![alt text][image8]

### Video

Below is the link to youtube video: 
https://www.youtube.com/watch?v=UqqVkZbjg6Q&feature=youtu.be


## Installation Instructions
Please use **one** of the two installation options, either native **or** docker installation.

### Native Installation

* Be sure that your workstation is running Ubuntu 16.04 Xenial Xerus or Ubuntu 14.04 Trusty Tahir. [Ubuntu downloads can be found here](https://www.ubuntu.com/download/desktop).
* If using a Virtual Machine to install Ubuntu, use the following configuration as minimum:
  * 2 CPU
  * 2 GB system memory
  * 25 GB of free hard drive space

  The Udacity provided virtual machine has ROS and Dataspeed DBW already installed, so you can skip the next two steps if you are using this.

* Follow these instructions to install ROS
  * [ROS Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu) if you have Ubuntu 16.04.
  * [ROS Indigo](http://wiki.ros.org/indigo/Installation/Ubuntu) if you have Ubuntu 14.04.
* [Dataspeed DBW](https://bitbucket.org/DataspeedInc/dbw_mkz_ros)
  * Use this option to install the SDK on a workstation that already has ROS installed: [One Line SDK Install (binary)](https://bitbucket.org/DataspeedInc/dbw_mkz_ros/src/81e63fcc335d7b64139d7482017d6a97b405e250/ROS_SETUP.md?fileviewer=file-view-default)
* Download the [Udacity Simulator](https://github.com/udacity/CarND-Capstone/releases).

### Docker Installation
[Install Docker](https://docs.docker.com/engine/installation/)

Build the docker container
```bash
docker build . -t capstone
```

Run the docker file
```bash
docker run -p 4567:4567 -v $PWD:/capstone -v /tmp/log:/root/.ros/ --rm -it capstone
```

### Port Forwarding
To set up port forwarding, please refer to the [instructions from term 2](https://classroom.udacity.com/nanodegrees/nd013/parts/40f38239-66b6-46ec-ae68-03afd8a601c8/modules/0949fca6-b379-42af-a919-ee50aa304e6a/lessons/f758c44c-5e40-4e01-93b5-1a82aa4e044f/concepts/16cf4a78-4fc7-49e1-8621-3450ca938b77)

### Usage

1. Clone the project repository
```bash
git clone https://github.com/udacity/CarND-Capstone.git
```

2. Install python dependencies
```bash
cd CarND-Capstone
pip install -r requirements.txt
```
3. Make and run styx
```bash
cd ros
catkin_make
source devel/setup.sh
roslaunch launch/styx.launch
```
4. Run the simulator

### Real world testing
1. Download [training bag](https://s3-us-west-1.amazonaws.com/udacity-selfdrivingcar/traffic_light_bag_file.zip) that was recorded on the Udacity self-driving car.
2. Unzip the file
```bash
unzip traffic_light_bag_file.zip
```
3. Play the bag file
```bash
rosbag play -l traffic_light_bag_file/traffic_light_training.bag
```
4. Launch your project in site mode
```bash
cd CarND-Capstone/ros
roslaunch launch/site.launch
```
5. Confirm that traffic light detection works on real life images
