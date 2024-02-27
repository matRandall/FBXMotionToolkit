# FBXMotionToolkit
Welcome to the FBXMotionToolKit a Python module for extracting, cleaning up, analysing and working human or character motion data within FBX files.  This module can be used to do the following:

- Extract rotation and translation joint data, in global and local space.
- Cleanup motion data by filling gaps using interpolation and smoothing using the butterworth filter
- Convert rotational joint data into different representations such as rotational matrix and quaternion.
- Measure the similarity of motions
- Timewarp motions
- Save rotational data in .csv files
- Save cleaned up or edited animations as FBX files

# Getting Started

## Installation

This module utilises Autodesk's freely FBX Python SDK which can be installed using the following steps:

1. Create a Python environment that matches the requirements of the Python FBX SDK version you are using.  This module was developed using FBX SDK version 2020.3.4, which requires Python 3.10 64bit to run.  It is recommended that you use Anaconda to do this to help manage your environments.
2. Install pip and wheel modules. (hint: Anaconda does this for you automatically whenever you create a new Python environment)
3. Download and install the FBX Python SDK for your operating system from the following url: <a href="https://aps.autodesk.com/developer/overview/fbx-sdk"> https://aps.autodesk.com/developer/overview/fbx-sdk </a>.  Note you need the FBX Python SDK is listed further down the page, not the standard SDK.
4. Go to FBX Python SDK installation folder containing the .whl file and run the following command to install the SDK in your environment: <code>python -m pip install name_of_the_wheel_file.whl</code>.

More information on installing and using the FBX Python SDK can be found here: <a href="https://help.autodesk.com/view/FBX/2020/ENU/?guid=FBX_Developer_Help_scripting_with_python_fbx_html">https://help.autodesk.com/view/FBX/2020/ENU/?guid=FBX_Developer_Help_scripting_with_python_fbx_html</a>.

## Basic Usage

A simple example of the FBXMotionToolkit in use can be seen below, where it is being used to extract Euler joint rotations and export them as .csv file.

```
import FBXMotionToolkit as fmt

# Specify paths to fbx motion file and joint map file
sampleDataFolder = r'C:\TestFolder\\'
motionFile = sampleDataFolder + "walk.fbx"
jointMapFile = sampleDataFolder + "viconMap.csv"

# Load the motion sequence, returning an FBXSequence object.
seq = fmt.importFBXSequence(motionFile)

# Map joints in the motion to joint names defined within the toolkit, using the jointMapFile. 
seq.mapJoints(jointMapFile)

# determine the end time of the motion based on the last key frame in the x-axis of the root joint.
endTime = seq.getTimeOfLastKey(fmt.joint.root, fmt.animationCurveType.ROTATION, fmt.axis.X)

# resample the entire motion at 120 frames per second, to fill in gaps in data or redundent axis.
seq.resample(120, endTime)

# Extract joint Euler rotation data for defined set of joints into a jointData object which simplifies working with joint data.
jointList = [fmt.joint.rhip, fmt.joint.lhip]
jointEulers = seq.getJointRotationAsEulers(jointList)

# Export joints rotations as a CSV file.
jointEulers.exportJointDataCSV(sampleDataFolder + "csvData.csv")

# remove sequence from memory.
seq.destroy()
```

## Documentation
- <a href="docs/InitialisingFBXSequenceObject.md">Initialising FBXSequence object</a>
- <a href="docs/FBXSequenceClass.md">FBXSequence class</a>
- <a href="docs/JointDataClass.md">JointData class</a>
- <a href="docs/SimilarityModule.md">SimilarityTools module</a>
- <a href="docs/TimeWarping.md">TimewarpingTools module</a>
