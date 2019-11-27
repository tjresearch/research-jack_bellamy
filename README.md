# research-jack_bellamy
research-jack_bellamy created by GitHub Classroom
Animal Object Detection via Custom Darknet

This project aims to use a custom trained neural network to quickly and accurately identify certain animals in images and display results in an easy to read format.

Requirements
-Linux
-Python 3
-CUDA 10.0 or later (for training)
-cuDNN 7.0 or later (for training)
-OpenCv 2.4 or later (for training)

Installation Instructions
-Download darknet directory and associated python files
Run Instructions
-Run command ./darknet detector train trainer.data yolov3.cfg darknet53.conv.74 to begin training images in directory build/darknet/x64/data/iamges
-To run the GUI, download both gui_test.py and day_nightv2.py, and run gui_test.py
