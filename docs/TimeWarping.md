# Time Warping

## Timewarp Class

The FBXMotionToolkit.Timewarp class, performs a dynamic time warp to temporally map the features of an input motion to that of a target motion.  The mapping is applied to the input motion using the FBXSequence.applyTimewarp() function.

The class utilises functions from the similarity and time warping modules, to preform the time warping.

### Constructor 

> TimewarpObject fmt.timewarp(inputJointData, targetJointData)

Performs a dynamic timewarp to create an alignment map aligning the input joint data to the target joint data.  The functions returns a timewarp object, containing an alignment map, which is used to warp the input motion. 

Parameters:

| Name            | Data Type | Description                      |
|-----------------|-----------|----------------------------------|
| inputJointData  | jointData | An instance of a jointData Class | 
| targetJointData | jointData | An instance of a jointData Class |

Data Requirements:

Both jointData objects must support the getDifferenceBetweenFrames() function, be of the same type, and contain the same joints.

Example:
```
import FBXMotionToolkit as fmt

# Open motions and map joints
motion1 = fmt.importFBXSequence("3_Jumps_01.fbx")
motion2 = fmt.importFBXSequence("3_Jumps_02.fbx")
motion1.mapJoints("jointMap.csv")
motion2.mapJoints("jointMap.csv")

# Get joint data
joints = [fmt.joint.rhip, fmt.joint.lhip, fmt.joint.rshoulder, fmt.joint.lshoulder]
jointQ1 = motion1.getJointRotationAsQuaternions(joints)
jointQ2 = motion2.getJointRotationAsQuaternions(joints)

# Perform DTW Alignment
tw = fmt.Timewarp(jointQ1, jointQ2)
motion1.applyTimewarp(tw.DTWremap)
motion1.export("aligned.fbx")

# Destroy Motions
motion1.destroy()
motion2.destroy()
```

## Properties

| Name                  | Data Type   | Description                                                                                                                                                                                        |
|-----------------------|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| costMatrix            | numpy array | Cost matrix of difference between every combination of input and target motion frames.  Array shape is (m, n), where m and n are the number of frames in the input and target motion respectively. |
| accumulatedCostMatrix | numpy array | The values in the cost matrix accumulated, starting from cell (0,0) to cell (m,n).  Array shape is (m, n), where m and n are the number of frames in the input and target motion respectively.     |
| DTWremap              | Int List    | A monotonic sequence of input frames that will result in a motion that is the optimal match to the target motion, as determined using DTW.                                                         |

### graphTimewarp

> void graphTimewarp()

Plots the alignment path determined by the timewarp on top of a heatmap showing the accumulated cost matrix. 

Example:
```
tw = fmt.Timewarp(jointQ1, jointQ2)
tw.graphTimewarp()
```

## Timewarp module

This module contains the functions for accumulating the cost matrix and plotting alignment, as used by the FBXMotionToolkit.Timewarp class.  This allows time warping algorithms to be implemented based on different methods of cost accumulation and alignment path plotting.

The functions are pre-imported into the FBXMotionToolkit and can be access as FBXMotionToolkit.tw.

### accumulatedCostMatrix

> numpyArray accumulatedCostMatrix(costMatrix)

Returns an accumulated cost matrix in which the values in the cost matrix are accumulated, starting from cell (0,0) to cell (m,n). It returns a numpy array of the same shape as the cost matrix

Parameters:

| Name                  | Data Type   | Description                                                                                                                                                                                        |
|-----------------------|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| costMatrix            | numpy array | Cost matrix of difference between every combination of input and target motion frames.  Array shape is (m, n), where m and n are the number of frames in the input and target motion respectively. |

### plotDTW

> intList plotDTW(accumulatedCostMatrix)

Returns A monotonic sequence of input frames that will result in a motion that is the optimal match to the target motion, as determined using DTW.

Parameters:

| Name                  | Data Type   | Description                                                                                                                                                                                                 |
|-----------------------|-------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| accumulatedCostMatrix | numpy array | A cost matrix in which the values have been accumulated, starting from cell (0,0) to cell (m,n).  Array shape is (m, n), where m and n are the number of frames in an input and target motion respectively. |

### graphDTW(matrix, DTWmap=intList)

Plots a heatmap showing a cost matrix or accumulated cost matrix.  It also allows an alignment path to be plotted on top of the heat map.

Parameters:

| Name   | Data Type   | Description                                                                                                                                |
|--------|-------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| matrix | numpy array | A cost matrix or accumulated cost matrix.                                                                                                  |
| DTWMap | Int List    | A monotonic sequence of input frames that will result in a motion that is the optimal match to the target motion, as determined using DTW. |

### Example

This example demonstrates the functions of the timewarp module being used to perform a DTW time warp and graph the results.

```

import FBXMotionToolkit as fmt

# Open motions and map joints
motion1 = fmt.importFBXSequence("3_Jumps_01.fbx")
motion2 = fmt.importFBXSequence("3_Jumps_02.fbx")
motion1.mapJoints("jointMap.csv")
motion2.mapJoints("jointMap.csv")

# Get joint data
joints = [fmt.joint.rhip, fmt.joint.lhip, fmt.joint.rshoulder, fmt.joint.lshoulder]
jointQ1 = motion1.getJointRotationAsQuaternions(joints)
jointQ2 = motion2.getJointRotationAsQuaternions(joints)

# Perform DTW Alignment using timewarp module
costMatrix = fmt.st.getSimilarityMatrix(jointQ1, jointQ2)
accumulatedCostMatrix = fmt.tw.accumulatedCostMatrix(costMatrix)
map = fmt.tw.plotDTW(accumulatedCostMatrix)
motion1.applyTimewarp(map)
motion1.export("aligned.fbx")

fmt.tw.graphDTW(accumulatedCostMatrix, DTWmap=map)

# Destroy Motions
motion1.destroy()
motion2.destroy()

```