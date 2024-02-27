# Similarity Module

This module contains functions for measuring the similarity of two motions, based on joint data contained in Joint Data Classes.  The functions are pre-imported into the FBXMotionToolkit and can be access as FBXMotionToolkit.st.

Each function has it own particular data requirements which need to be considered.  These are documented within the description of each function.

### measureDistanceSimilarity

> float measureDistanceSimilarity(inputJointData, targetJointData)

Measures the similarity of two motions stored in jointData classes.  The function uses the getDifferenceBetweenFrames() function of the jointData class.  The similarity score returned $d$ is $d = t/(j*f)$ where $t$ is the total difference between the two motions, $j$ is the number of joints in jointData objects, and $f$ is the number of frames in the joint data objects.

Data requirements:

Both jointData objects must support the getDifferenceBetweenFrames() function, be of the same type, and contain the same joints and frames.

Parameters:

| Name            | Data Type | Description                      |
|-----------------|-----------|----------------------------------|
| inputJointData  | jointData | An instance of a jointData Class | 
| targetJointData | jointData | An instance of a jointData Class |

Example:
```
import FBXMotionToolkit as fmt

# Open motions and map joints
motion1 = fmt.importFBXSequence("3_Jumps_01.fbx")
motion2 = fmt.importFBXSequence("3_Jumps_02.fbx")
motion1.mapJoints("jointMap.csv")
motion2.mapJoints("jointMap.csv")

# Match duration of motions using UTW
motion1Duration = motion1.getTimeOfLastKey(fmt.joint.root, fmt.animationCurveType.ROTATION, fmt.axis.x)
motion2Duration = motion2.getTimeOfLastKey(fmt.joint.root, fmt.animationCurveType.ROTATION, fmt.axis.x)
motion1.UTW(motion1Duration, motion2Duration, 120)

# get joint data
joints = [fmt.joint.rhip, fmt.joint.lhip, fmt.joint.rshoulder, fmt.joint.lshoulder]
jointQ1 = motion1.getJointRotationAsQuaternions(joints)
jointQ2 = motion2.getJointRotationAsQuaternions(joints)

# measure similarity using distance based metric
d = fmt.st.measureDistanceSimilarity(jointQ1, jointQ2)
```

### measureCorrelationSimilarity

> float measureCorrelationSimilarity(inputFlatJointData,targetFlatJointData, method, minThreshold=float)

Measures the similarity of two motions based on the correlations of joint parameters.  The function uses flattened joint data as obtained using the getFlatJointData() function on a joint data object.  Function can be used to evaluate the correlation of joints within the same motion as well as between separate motions.  The similarity score returned is the average correlation across all joint parameters.

Data requirements:

Both flattened joint data arrays must contain the same number of joint parameters and frames.

Parameters:

| Name                | Data Type   | Description                                                                                                                                     |
|---------------------|-------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| inputFlatJointData  | Numpy Array | Flattened two dimensional numpy array of shape (joint parameters, frames)                                                                       | 
| targetFlatJointData | Numpy Array | Flattened two dimensional numpy array of shape (joint parameters, frames)                                                                       |
| method              | String      | Pearson, Spearman or Kendall Tau.  Enumerated in using st.CorrelationMethod class.                                                              |
| minThreshold        | Float       | Optional argument, default = 0.001.  Joint parameters with a variance below the specified minimum threshold are given a correlation score of 1. |

Example:
```
import FBXMotionToolkit as fmt

# Open motions and map joints
motion1 = fmt.importFBXSequence("3_Jumps_01.fbx")
motion2 = fmt.importFBXSequence("3_Jumps_02.fbx")
motion1.mapJoints("jointMap.csv")
motion2.mapJoints("jointMap.csv")

# Match duration of motions using UTW
motion1Duration = motion1.getTimeOfLastKey(fmt.joint.root, fmt.animationCurveType.ROTATION, fmt.axis.x)
motion2Duration = motion2.getTimeOfLastKey(fmt.joint.root, fmt.animationCurveType.ROTATION, fmt.axis.x)
motion1.UTW(motion1Duration, motion2Duration, 120)

# get joint data
joints = [fmt.joint.rhip, fmt.joint.lhip, fmt.joint.rshoulder, fmt.joint.lshoulder]
jointQ1 = motion1.getJointRotationAsQuaternions(joints)
jointQ2 = motion2.getJointRotationAsQuaternions(joints)

# measure similarity using correlation based metric
jointQ1flat = jointQ1.getFlatJointData()
jointQ2flat = jointQ2.getFlatJointData()
c = fmt.st.measureCorrelationSimilarity(jointQ1flat, jointQ2flat, fmt.st.CorrelationMethod.Pearson)
```

### getSimilarityMatrix

> numpyArray getSimilarityMatrix(inputJointData, targetJointData)

Returns a cost matrix of difference between every combination of input and target motion frames stored in joint data classes.  The function uses the getDifferenceBetweenFrames() function of the jointData class.

Data requirements:

Both jointData objects must support the getDifferenceBetweenFrames() function, be of the same type and contain the same joints.

Parameters:

| Name            | Data Type | Description                      |
|-----------------|-----------|----------------------------------|
| inputJointData  | jointData | An instance of a jointData Class | 
| targetJointData | jointData | An instance of a jointData Class |

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
costMatrix = fmt.st.getSimilarityMatrix(jointQ1, jointQ2)
```