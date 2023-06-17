
# Driver Drowsiness Detection System

## Overview

This project aims to develop a driver drowsiness detection system using machine learning and Python Flask. The system utilizes yawn count and eye closure ratio to accurately detect the drowsiness of the driver in real time.

## Features

- Real-time driver drowsiness detection
- Accurate detection using yawn count and eye closure ratio
- User-friendly web interface built with Python Flask

## Requirements

- Python 3.x
- Flask
- OpenCV
- dlib
- numpy

## Installation

1. Clone the repository:
   > git clone https://github.com/TheArushiSingh/Driver-Drowsiness-Detection-System.git
   
3. Install the required dependencies:
   > pip install -r requirements.txt

4. Run the application:

   > python main.py

5. Open a web browser and go to `http://localhost:5000` to access the application.

## Usage

1. Start the application by running `main.py`.
2. Ensure that your webcam is connected and functioning properly.
3. Open a web browser and navigate to the provided URL.
4. The webcam feed will be displayed on the web interface.
5. The system will continuously monitor the driver's face and analyze their eye closure ratio and yawn count.
6. If the system detects significant drowsiness, an alert will be triggered.
7. The alert is in the form of an audible alarm.
8. Take appropriate action based on the alert to prevent any potential accidents caused by drowsy driving.


## Methodolgy 

### Drowsiness Detection Using CNN
- To detect eye and mouth states, a Modified CNN model is used.
- Four convolutional layers with increasing filters and max pooling layers are used to reduce spatial dimensions
- The first convolutional layer has 16 filters and a 3x3 kernel size, which means that it will apply 16 different 3x3 filters to the input image to detect various features such as edges, corners, and blobs.
- The second convolutional layer has 32 filters and a 3x3 kernel size. It will receive the output from the first layer and apply 32 different 3x3 filters to the feature maps to detect more complex patterns and textures. The max pooling layer with a 2x2 pool size is applied after the second convolutional layer to reduce the spatial dimensions and increase the model's ability to generalize to new data.
- Batch normalization is used after the second convolutional layer to speed up convergence and avoid overfitting
- After the third convolutional layer, a maximum pooling layer with 2x2 pool size and batch normalization is added
- The fourth convolutional layer has batch normalization, a max pooling layer with a 2x2 pool size, and 128 filters on a 3x3 kernel
- The final convolutional layer’s flattened output is fed into a fully connected layer with 128 neurons and ReLU activation
- Batch normalization is applied, and the final layer is a dropout layer with a dropout rate of 0.25
- Each of the four classes (No-Yawn, Yawn, Closed, and Open) is represented by a single neuron in the output layer, which uses a softmax activation function to predict the probabilities for each class

### Dataset Used
The dataset utilised for the research is ``yawn-eye-dataset-new" dataset from Kaggle consisting of 2900 images splitted into four categories i.e.open eyes (726 images; 617 training and 109 test samples), closed eyes (726 images; 617 training and 109 test samples), yawn (723 images; 617 training and 106 test samples), and no yawn (725 images; 616 training and 109 test samples).

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch.
3. Make your changes and enhancements.
4. Test your changes thoroughly.
5. Submit a pull request detailing your changes.
