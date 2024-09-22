# Real-Time Object Measurement Using Webcam and Mobile Camera

Project Video-> https://drive.google.com/file/d/17AqEPnFRhihOFp5P40NwGmXovuixFekh/view?usp=sharing

This project provides real-time object measurement using either a webcam or a mobile phone camera. The application can also process images from a directory and measure object dimensions using contours and bounding boxes. It calculates the width and height of objects based on a reference object with a known width.

Features->

Real-time object detection and measurement using a webcam.
Option to use a mobile phone camera (via the IP Webcam app) as an external video input.
Object measurement from system images.
Contour detection and measurement with pixel-to-metric conversion based on a reference object.

Technologies Used->

Python
OpenCV
Matplotlib
NumPy
IP Webcam (for mobile camera streaming)

Installation->
Prerequisites:

Ensure that you have the following installed on your system:

Python 3.x
OpenCV: pip install opencv-python
Matplotlib: pip install matplotlib
NumPy: pip install numpy

IP Webcam Setup (For Mobile Camera)->

Install IP Webcam from the Google Play Store on your mobile device.
Open the app and start the server.
Note the IP address shown at the bottom of the screen (e.g., http://192.168.X.X:8080/video).

Run the script:

python object_measurement.py
Select an input source:

Press w to capture objects from the webcam.
Press m to capture objects using a mobile camera (via the IP Webcam app).
Press i to choose an image from your system for object measurement.

Mobile Camera (IP Webcam):

If you choose m, you will be prompted to enter the IP address of your mobile camera.
Example: http://192.168.X.X:8080/video

Images:

If you choose i, you will be prompted to enter the path of the directory containing the images.
You can then select an image from the directory for object measurement.
Exiting:

To stop the live feed from the webcam or mobile camera, press q.

How It Works
Webcam: The program captures frames from the webcam, processes them to detect contours, and calculates the dimensions of objects by converting pixels to millimeters based on the reference object.

Mobile Camera: By connecting your mobile phone as a remote camera using IP Webcam, the program receives the live feed via the network and processes the video for object measurement.

Image Directory: You can select an image from a directory, and the program will detect the objects in the image and measure them.

Configuration

Reference Object Width: The default reference object width is set to 50.0 mm. You can modify this in the code to match your reference object.
Customization
Change Reference Width: In the main code, change the reference_width variable to match the actual width of your reference object in millimeters.

reference_width = 50.0  # Set your reference width here
Adjust Contour Detection: You can modify the contour detection thresholds by changing the cv2.Canny() parameters in the code.

Example
Select the input source:

Enter 'w' for webcam, 'm' for mobile camera, or 'i' for images: m
Enter the mobile camera IP address:

Enter the IP address of the mobile camera (e.g., http://192.168.X.X:8080/video): http://192.168.X.X:8080/video
