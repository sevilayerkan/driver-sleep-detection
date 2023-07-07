# Driver Sleep Detection

## Project Details

🎯 The Driver Sleep Detection App is a web-based application that uses computer vision techniques to track alertness based on eye and mouth movement. It detects closed eyes and yawning in real-time using OpenCV and dlib libraries.

## Features

- Real-time video feed with alertness tracking
- Alert notifications for closed eyes and yawning

## Prerequisites

- Python 3.7 or higher
- Webcam connected to the system

## Installation

Make sure Python and pip is installed by using this commands in your command line

```bash
python --version
pip --version
```

If they are installed use this to install the requirements:

```bash
pip install -r requirements.txt
```

Download the shape predictor model:

- Download the shape predictor model (shape_predictor_68_face_landmarks.dat) from this link: shape_predictor_68_face_landmarks.dat.
- Extract the downloaded file.
- Copy the [shape_predictor_68_face_landmarks.dat](https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2) file and paste it into the project directory.


## Usage for Flask Web App

### Requirements

- Python 3.6 or higher

### Installation

0. Clone repo in your device

1. Navigate to the project directory:

   ```shell
   cd docker-file-generator
   ```

2. Create a virtual environment (optional but recommended):

   ```shell
   python3 -m venv venv
   ```

3. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

### Usage

1. Run the Flask application:

   ```shell
   flask run
   ```

2. Open your web browser and go to `http://localhost:5000`.

3. You will see the video feed with real-time alertness tracking. The application will display alerts on the video when closed eyes or yawning are detected.

4. Press Ctrl+C in the terminal to stop the application.
