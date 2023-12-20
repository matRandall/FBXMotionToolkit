# FBXMotionToolkit
Welcome to the FBXMotionToolKit a Python module for extracting, cleaning up, anlysing and working human or character motion data within FBX files.  This module can be used to do the following:

- Extract rotation and translation joint data, in global and local space.
- Cleanup motion data by filling gaps using interpolation and smoothing using the butterworth filter
- Convert rotational joint data into different representations such as rotational matrix and quaternion.
- Measure the similarity of motions
- Timewarp motions
- Save rotational data in .csv files
- Save cleaned up or edited animations as FBX files

# Getting Started

## Installation

This module utilises Autodesk's freely Python FBX SDK which can be installed using the following steps:

1. Create a Python environment that matches the requirements of the Python FBX SDK version you are using.  This module was developed using FBX SDK version 2020.3.4, which requires Python 3.10 64bit to run.  It is recommended that you use Anaconda to do this to help manage your environments.
2. Install pip and wheel modules. (hint: Anaconda does this for you automatically whenever you create a new Python environment)
3. Download and install the FBX Python SDK for your operating system from the following url: <a href="https://aps.autodesk.com/developer/overview/fbx-sdk"> https://aps.autodesk.com/developer/overview/fbx-sdk </a>
