# Parking Spot Detection System

This project is a parking spot monitoring system developed using OpenCV in Python. It analyzes video footage of a parking lot to detect empty and occupied parking spots in real-time.

## Features

- Detects parking spots using connected components analysis
- Tracks changes in parking spot occupancy between frames
- Provides real-time visualization of parking spot status
- Calculates and displays the number of available parking spots

## Preview 
![image](https://github.com/zain-0/Parking-Spot-Detection-Using-OpenCV/assets/144730764/e493c1a1-0338-4443-bac0-af6991d9837f)


## Prerequisites

- Python 3.7 or later
- OpenCV library (`cv2`)
- NumPy library (`numpy`)

## Installation

1. Clone the repository:
git clone https://github.com/zain-0/parking-spot-Detection-Using-OpenCV.git


2. Install the required libraries:

pip install opencv-python numpy

## Usage

1. Place your video file (`parking_1920_1080_loop.mp4`) in the project directory.
2. Create a binary mask image (`mask_1920_1080.png`) representing the parking spots.
3. Update the `video_path` and `mask` variables in the script with the correct file paths.
4. Run the script:
  main.py
5. Press 'q' to exit the application.


