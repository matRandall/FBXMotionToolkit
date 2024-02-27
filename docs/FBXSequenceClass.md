# FBXSequence Class

An FBX sequence class is created by calling the importFBXSequence() as described in the <a href="docs/Initialising FBXSequence object.md">Initialising FBXSequence object</a> document.  Once created the class provides a number of functions to be read, manipulate and exported.

## Properties


| Name         | Data Type         | Description                                                                                                               |
|--------------|-------------------|---------------------------------------------------------------------------------------------------------------------------|
| file         | String            | Path of the FBX file imported into the FBXSequence instance                                                               |
| jointNameMap | Python Dictionary | Python dictionary of standardised names (key) and fbx joint names <value> pairs                                           |
| fbxScene     | fbxScene object   | An FBX scene object with can be used directly with the FBX SDK to create additional functionality to the FBXMotionToolkit |.

## FBX File Functions

### mapJoints

> void FBXSequence.mapJoints(JointMapFilePath)

Maps the joints within an FBX file to a standard set of joint names used by the FBXMotionToolkit.  This is a critical step in initialising an FBXSequence object and is described in more detail in the <a href="docs/Initialising FBXSequence object.md">Initialising FBXSequence object</a> document.

Parameters:

| Name             | Data Type | Description                                         |
|------------------|-----------|-----------------------------------------------------|
| JointMapFilePath | String    | Full file name with path of the .csv joint map file |

Example:
```
myFBX.mapJoints(r'C:\jointMapFile.csv')
```

### printSceneHierarchy

> void FBXSequence.printSceneHierarchy(void)

Prints the hierarchy of the objects within the FBX file.  This can be used to determine joint names within the FBX file for use in the joint map.

Example:
```
myFBX.printSceneHierarchy()
```
Result:
```commandline
char1
   Solving
      Hips
         Spine
            Spine1
               Spine2
                  Spine3
                     Neck
                        Neck1
                           Head
                              HeadEnd
                     RightShoulder
                        RightArm
                           RightForeArm
                              RightHand
                                 RightHandThumb1
                                 RightHandMiddle1
                     LeftShoulder
                        LeftArm
                           LeftForeArm
                              LeftHand
                                 LeftHandThumb1
                                 LeftHandMiddle1
         RightUpLeg
            RightLeg
               RightFoot
                  RightForeFoot
                     RightToeBase
                        RightToeBaseEnd
         LeftUpLeg
            LeftLeg
               LeftFoot
                  LeftForeFoot
                     LeftToeBase
                        LeftToeBaseEnd
```
### exportJointData

> void FBXSequence.exportJointInfo(outputFile)

Exports information on every mapped joint map as a .csv file.  Exports the following for each joint: standardised name, name in FBX file, rotation order, number of key frames in the XYZ axis of the joint's translation and rotation, and the position of the joint's last key frame in seconds.

Parameters:

| Name       | Data Type | Description                                      |
|------------|-----------|--------------------------------------------------|
| outputFile | String    | Full file name with path for exporting .csv file |

Example:
```
myFBX.exportJointInfo(r'C:\jointInfo.csv')
```

### export

> void FBXSequence.export(outputFile)

Exports the FBXSequence as a .fbx file.

Parameters:

| Name       | Data Type | Description                                      |
|------------|-----------|--------------------------------------------------|
| outputFile | String    | Full file name with path for exporting .fbx file |

Example:
```
myFBX.export(r'C:\motionFile.fbx')
```

### destroy

> void FBXSequence.destroy()

Destroy FBX sequence and free up computer memory.

Example:
```
myFBX.destroy()
```

## Joint Information Functions

### getTimeOfLastKey

> float FBXSequence.getTimeOfLastKey(joint, animationType, axis)

Get the time of the last key frame in a joint animation curve in seconds.

Parameters:

| Name          | Data Type | Description                                                                                                                                                                        |
|---------------|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| joint         | String    | The name of joint to read the last key frame from.  Specified using standardised joint names in FBXMotionToolkit.joint class.                                                      |
| animationTYpe | String    | The type of animation curve (translation or rotation) to read the last key frame from.  Specified using standardised animation types in FBXMotionToolkit.animationCurveType class. |
| axis          | Int       | The axis to read the last key frame from.  Specified using standardised axis indexes (x=0, y=1, z=0) as specified in FBXMotionToolkit.axis class.                                  |

Returns:

float: Time in seconds

Example:
```
import FBXMotionToolkit as fmt

myFBX = fmt.importFBXSequence(r'C:\motionFile.fbx')
myFBX.mapJoints(r'C:\jointMapFile.csv')
animationDuration = myFBX.getTimeOfLastKey(fmt.joint.rhip, fmt.animationCurveType.ROTATION, fmt.axis.x)
```

### getJointKeyTimes

> float list FBXSequence.getJointKeyTimes(joint, animationType, axis)

Get the times of each key frame in a joint animation curve in seconds.

Parameters:

| Name          | Data Type | Description                                                                                                                                                              |
|---------------|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| joint         | String    | The name of joint to get key times from.  Specified using standardised joint names in FBXMotionToolkit.joint class.                                                      |
| animationTYpe | String    | The type of animation curve (translation or rotation) to get key times from.  Specified using standardised animation types in FBXMotionToolkit.animationCurveType class. |
| axis          | Int       | The axis to get key times from.  Specified using standardised axis indexes (x=0, y=1, z=0) as specified in FBXMotionToolkit.axis class.                                  |

Returns:

float list: A list of times in seconds

Example:
```
import FBXMotionToolkit as fmt

myFBX = fmt.importFBXSequence(r'C:\motionFile.fbx')
myFBX.mapJoints(r'C:\jointMapFile.csv')
keyTimes = myFBX.getJointKeyTimes(fmt.joint.rhip, fmt.animationCurveType.ROTATION, fmt.axis.x)
```

### getNumberKeyframes

> int FBXSequence.getNumberKeyframes(joint, animationType, axis)

Get the number of key frames in a joint animation curve.

Parameters:

| Name          | Data Type | Description                                                                                                                                                                    |
|---------------|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| joint         | String    | The name of joint to get key frame count from.  Specified using standardised joint names in FBXMotionToolkit.joint class.                                                      |
| animationTYpe | String    | The type of animation curve (translation or rotation) to get key frame count from.  Specified using standardised animation types in FBXMotionToolkit.animationCurveType class. |
| axis          | Int       | The axis to get ket frame count from.  Specified using standardised axis indexes (x=0, y=1, z=0) as specified in FBXMotionToolkit.axis class.                                  |

Returns:

int: Number of key frames in animation curve

Example:
```
import FBXMotionToolkit as fmt

myFBX = fmt.importFBXSequence(r'C:\motionFile.fbx')
myFBX.mapJoints(r'C:\jointMapFile.csv')
keyCount = myFBX.getNumberKeyframes(fmt.joint.rhip, fmt.animationCurveType.ROTATION, fmt.axis.x)
```

### getFramesPerSecond

> int FBXSequence.getFramesPerSecond(joint, animationType, axis)

Get the frame rate of the animation curve, based on the first two keys in the animation curve.  Output is rounded to the nearest whole number.

Parameters:

| Name          | Data Type | Description                                                                                                                                                         |
|---------------|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| joint         | String    | The name of joint to read fps from.  Specified using standardised joint names in FBXMotionToolkit.joint class.                                                      |
| animationTYpe | String    | The type of animation curve (translation or rotation) to read fps from.  Specified using standardised animation types in FBXMotionToolkit.animationCurveType class. |
| axis          | Int       | The axis to read the fps from.  Specified using standardised axis indexes (x=0, y=1, z=0) as specified in FBXMotionToolkit.axis class.                              |

Returns:

int: Frame rate of the animation curve, rounded to the nearest whole number.

Example:
```
import FBXMotionToolkit as fmt

myFBX = fmt.importFBXSequence(r'C:\motionFile.fbx')
myFBX.mapJoints(r'C:\jointMapFile.csv')
orderOfRotation = myFBX.getFramesPerSecond(fmt.joint.rhip, fmt.animationCurveType.ROTATION, fmt.axis.x)
```

### getRotationOrder

> string FBXSequence.getRotationOrder(joint)

Get the rotation order of a given joint.

Parameters:

| Name         | Data Type  | Description                                                                                                                  |
|--------------|------------|------------------------------------------------------------------------------------------------------------------------------|
| joint        | String     | The name of joint to get the rotation order from.  Specified using standardised joint names in FBXMotionToolkit.joint class. |

Returns:

string: String specifying the order of the rotations e.g 'xyz'.

Example:
```
import FBXMotionToolkit as fmt

myFBX = fmt.importFBXSequence(r'C:\motionFile.fbx')
myFBX.mapJoints(r'C:\jointMapFile.csv')
myInt = myFBX.getRotationOrder(fmt.joint.rhip)
```

## Joint Manipulation Functions

### unrollJointAxis

> void FBXSequence.unrollJointAxis(joint, axis)

Unroll the values of key frames within a given joint's rotational axis.

Parameters:

| Name         | Data Type  | Description                                                                                                                 |
|--------------|------------|-----------------------------------------------------------------------------------------------------------------------------|
| joint        | String     | The name of joint to unroll.  Specified using standardised joint names in FBXMotionToolkit.joint class.                     |
| axis         | Int        | The axis to unroll.  Specified using standardised axis indexes (x=0, y=1, z=0) as specified in FBXMotionToolkit.axis class. |

Example:
```
import FBXMotionToolkit as fmt

myFBX = fmt.importFBXSequence(r'C:\motionFile.fbx')
myFBX.mapJoints(r'C:\jointMapFile.csv')
myFBX.unrollJointAxis(fmt.joint.root, fmt.axis.x)
```

### unrollJoint

> void FBXSequence.unrollJointAxis(joint)

Unroll the values of key frames within all rotational axes of a given joint.

Parameters:

| Name         | Data Type  | Description                                                                                             |
|--------------|------------|---------------------------------------------------------------------------------------------------------|
| joint        | String     | The name of joint to unroll.  Specified using standardised joint names in FBXMotionToolkit.joint class. |


Example:
```
import FBXMotionToolkit as fmt

myFBX = fmt.importFBXSequence(r'C:\motionFile.fbx')
myFBX.mapJoints(r'C:\jointMapFile.csv')
myFBX.unrollJoint(fmt.joint.root)
```

### unrollAllJoints

> void FBXSequence.unrollAllJoints(void)

Unroll the values of key frames within rotational axis across all joints in the animation.

Example:
```
import FBXMotionToolkit as fmt

myFBX = fmt.importFBXSequence(r'C:\motionFile.fbx')
myFBX.mapJoints(r'C:\jointMapFile.csv')
myFBX.unrollAllJoints()
```

### makeJointsAnimatable

> void FBXSequence.makeJointAnimatable(joint, animationType)

If the given joint or list of joints are not already animated for a given animationType (rotation, translation), the joint is made animatable and a key frame is added to the animation curve.

Parameters:

| Name          | Data Type | Description                                                                                                                                                           |
|---------------|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| jointList     | String    | Joint name or list of joints.  Specified using standardised joint names in FBXMotionToolkit.joint class.                                                              |
| animationTYpe | String    | The type of animation curve (translation or rotation) to make animatable.  Specified using standardised animation types in FBXMotionToolkit.animationCurveType class. |

Example:
```
import FBXMotionToolkit as fmt

myFBX = fmt.importFBXSequence(r'C:\motionFile.fbx')
myFBX.mapJoints(r'C:\jointMapFile.csv')
myFBX.makeJointAnimatable(fmt.joint.rhip, fmt.animationCurveType.ROTATION)
```

### resample

> void FBXSequence.resample(fps, endTime)

Resamples all the animated axis of every joint in an FBXSequence at a given frame rate up to a specified duration.  The duration of animation curves will be expanded or truncated to fit the specified end time, resulting in key frames outside the duration being lost.  Unanimated joint axis are left unaltered.  To avoid aliasing issues, joints should be unrolled where necessary.

Parameters:

| Name    | Data Type | Description                                               |
|---------|-----------|-----------------------------------------------------------|
| fps     | Int       | The frame rate in frames per second                       |
| entTime | Float     | The duration of the resampled animation curves in seconds |

Example:
```
import FBXMotionToolkit as fmt

myFBX = fmt.importFBXSequence(r'C:\motionFile.fbx')
myFBX.mapJoints(r'C:\jointMapFile.csv')
duration = myFBX.getTimeOfLastKey(fmt.joint.root, fmt.animationCurveType.ROTATION, fmt.axis.x)
myFBX.resample(120, duration)
```

### UTW

> void FBXSequence.UTW(currentDuration, newDuration, fps)

UTW (Universal Time Warp), uniformly re-times all animation within the FBXSequence to fit a new duration, then resamples the animation at a new frame rate.  Unanimated joint axis are left unaltered.  To avoid aliasing issues, joints should be unrolled where necessary.

Parameters:

| Name            | Data Type | Description                                                        |
|-----------------|-----------|--------------------------------------------------------------------|
| currentDuration | Float     | The current duration of the animation in seconds                   |
| newDuration     | Float     | The new duration that the animation should be warped to in seconds |
| fps             | Int       | The frame rate in frames per second                                |

Example:
```
import FBXMotionToolkit as fmt

motion1 = fmt.importFBXSequence(r'C:\motionFile1.fbx')
motion1.mapJoints(r'C:\jointMapFile.csv')
duration1 = motion1.getTimeOfLastKey(fmt.joint.root, fmt.animationCurveType.ROTATION, fmt.axis.x)

motion2 = fmt.importFBXSequence(r'C:\motionFile2.fbx')
motion2.mapJoints(r'C:\jointMapFile.csv')
duration2 = motion2.getTimeOfLastKey(fmt.joint.root, fmt.animationCurveType.ROTATION, fmt.axis.x)

# Uniformally timewarp motion2 to match duration of motion1
motion2.resample(duration2, duration1, 120)
```

### applyTimewarp

> void FBXSequence.applyTimewarp(frameMap)

Applies a timewarp as specified in a frame map to all animated joints in the FBXSequence.  The timewarping tools module can be used create a frame map that is a DTW (Dynamic Timewarp) in which one motion is time warped to fit another.

Parameters:

| Name     | Data Type | Description                                              |
|----------|-----------|----------------------------------------------------------|
| frameMap | Int List  | A list of integers specifying a sequence of frame remaps | 

Example:
```
# Warps motion2 to fit motion1 using dynamic time warping
import FBXMotionToolkit as fmt

motion1 = fmt.importFBXSequence(r'C:\motionFile1.fbx')
motion1.mapJoints(r'C:\jointMapFile.csv')
duration1 = motion1.getTimeOfLastKey(fmt.joint.root, fmt.animationCurveType.ROTATION, fmt.axis.x)

motion2 = fmt.importFBXSequence(r'C:\motionFile2.fbx')
motion2.mapJoints(r'C:\jointMapFile.csv')
duration2 = motion2.getTimeOfLastKey(fmt.joint.root, fmt.animationCurveType.ROTATION, fmt.axis.x)

jointList = [fmt.joint.rhip, fmt.joint.lhip]
jointQuats = motion1.getJointRotationAsQuaternions(jointList)
jointQuats2 = motion2.getJointRotationAsQuaternions(jointList)

timewarp = fmt.timewarp(motion1, motion2)
motion2.applyTimewarp(tw.DTWremap)
motion2.export(sampleDataFolder + "warpedFile.fbx")
```

## Joint Data Extraction Functions

### getJointRotationAsEulers

> JointDataEulersObj FBXSequence.getJointRotationAsEulers(jointList)

Retrieves the rotation data for a single joint or list of joints as Eulers, returning the joint rotations for each joint on every frame in a single joint data object, which allows easier access and analysis of joint data.  

All joints must be animatable with key frames at matching times on all joint axis.  Use FBXSequence.makeJointAnimatable() and FBXSequence.resample() to make joints conform to one another.

Parameters:

| Name      | Data Type   | Description                                                                                                  |
|-----------|-------------|--------------------------------------------------------------------------------------------------------------|
| jointList | String List | A single joint or list of joints.  Specified using standardised joint names in FBXMotionToolkit.joint class. | 

Example:
```
# Loads then conforms motion data before extracting joint data as Eulars.
import FBXMotionToolkit as fmt

motion1 = fmt.importFBXSequence(r'C:\motionFile1.fbx')
motion1.mapJoints(r'C:\jointMapFile.csv')
duration1 = motion1.getTimeOfLastKey(fmt.joint.root, fmt.animationCurveType.ROTATION, fmt.axis.x)

jointList = [fmt.joint.rhip, fmt.joint.lhip]
motion1.makeJointsAnimatable(jointList, fmt.animationCurveType.ROTATION)
motion1.resample(120, seq1Duration)
jointEulers = motion1.getJointRotationAsEulers(jointList)
```

### getJointRotationAsQuaternions

> JointDataQuaternionsObj FBXSequence.getJointRotationAsQuaternions(jointList)

Retrieves the rotation data for a single joint or list of joints and converts joint angles to Quaternions, returning the joint rotations for each joint on every frame in a single joint data object, which allows easier access and analysis of joint data.  Rotation orders of each joint are inspected to ensure correct conversion. All quaternions for each joint are expressed within the same canonical single cover space.

All joints must be animatable with key frames at matching times on all joint axis.  Use FBXSequence.makeJointAnimatable() and FBXSequence.resample() to make joints conform to one another.

Parameters:

| Name      | Data Type   | Description                                                                                                  |
|-----------|-------------|--------------------------------------------------------------------------------------------------------------|
| jointList | String List | A single joint or list of joints.  Specified using standardised joint names in FBXMotionToolkit.joint class. | 

Example:
```
# Loads then conforms motion data before extracting joint data as Quaternions.
import FBXMotionToolkit as fmt

motion1 = fmt.importFBXSequence(r'C:\motionFile1.fbx')
motion1.mapJoints(r'C:\jointMapFile.csv')
duration1 = motion1.getTimeOfLastKey(fmt.joint.root, fmt.animationCurveType.ROTATION, fmt.axis.x)

jointList = [fmt.joint.rhip, fmt.joint.lhip]
motion1.makeJointsAnimatable(jointList, fmt.animationCurveType.ROTATION)
motion1.resample(120, seq1Duration)
jointQuats = motion1.getJointRotationAsQuaternions(jointList)
```

### getJointRotationAsMatrices

> JointDataMatricesObj FBXSequence.getJointRotationAsMatrices(jointList)

Retrieves the rotation data for a single joint or list of joints and converts joint angles to Matrices, returning the joint rotations for each joint on every frame in a single joint data object, which allows easier access and analysis of joint data.

All joints must be animatable with key frames at matching times on all joint axis.  Use FBXSequence.makeJointAnimatable() and FBXSequence.resample() to make joints conform to one another.

Parameters:

| Name      | Data Type   | Description                                                                                                  |
|-----------|-------------|--------------------------------------------------------------------------------------------------------------|
| jointList | String List | A single joint or list of joints.  Specified using standardised joint names in FBXMotionToolkit.joint class. | 

Example:
```
# Loads then conforms motion data before extracting joint data as Matrices.
import FBXMotionToolkit as fmt

motion1 = fmt.importFBXSequence(r'C:\motionFile1.fbx')
motion1.mapJoints(r'C:\jointMapFile.csv')
duration1 = motion1.getTimeOfLastKey(fmt.joint.root, fmt.animationCurveType.ROTATION, fmt.axis.x)

jointList = [fmt.joint.rhip, fmt.joint.lhip]
motion1.makeJointsAnimatable(jointList, fmt.animationCurveType.ROTATION)
motion1.resample(120, seq1Duration)
jointMatrices = motion1.getJointRotationAsMatrices(jointList)
```

### getJointRotationAsDisplacementVectors

> JointDataDisplacementVectorsObj FBXSequence.getJointRotationAsDisplacementVectors(jointList)

Retrieves the rotation data for a single joint or list of joints and converts joint angles to displacement vectors, returning the joint rotations for each joint on every frame in a single joint data object, which allows easier access and analysis of joint data.

A displacement vector is a unit length vector (x,y,z) in the same direction as the joint.

All joints must be animatable with key frames at matching times on all joint axis.  Use FBXSequence.makeJointAnimatable() and FBXSequence.resample() to make joints conform to one another.

Parameters:

| Name        | Data Type   | Description                                                                                                  |
|-------------|-------------|--------------------------------------------------------------------------------------------------------------|
| jointList   | String List | A single joint or list of joints.  Specified using standardised joint names in FBXMotionToolkit.joint class. | 
| sampleTimes | Float List  | A list of times in seconds.                                                                                  | 

Example:
```
# Loads then conforms motion data before extracting joint data as displacement vectors.
import FBXMotionToolkit as fmt

motion1 = fmt.importFBXSequence(r'C:\motionFile1.fbx')
motion1.mapJoints(r'C:\jointMapFile.csv')
duration1 = motion1.getTimeOfLastKey(fmt.joint.root, fmt.animationCurveType.ROTATION, fmt.axis.x)

jointList = [fmt.joint.rhip, fmt.joint.lhip]
motion1.makeJointsAnimatable(jointList, fmt.animationCurveType.ROTATION)
motion1.resample(120, seq1Duration)
jointDisplacementVectors = motion1.getJointRotationAsDisplacementVectors(jointList)
```

### getJointAsGlobalTranslations

> JointDataGlobalTranslationsObj FBXSequence.getJointAsGlobalTranslations(jointList, sampleTimes)

Retrieves the rotation data for a single joint or list of joints as positions in global space, returning the global joint positions for each joint for every time point specified in sampleTimes.  All positional data is returned in a single joint data object, which allows easier access and analysis of joint data.

All joints must be animatable with key frames at matching times on all joint axis.  Use FBXSequence.makeJointAnimatable() and FBXSequence.resample() to make joints conform to one another.

Parameters:

| Name        | Data Type   | Description                                                                                                  |
|-------------|-------------|--------------------------------------------------------------------------------------------------------------|
| jointList   | String List | A single joint or list of joints.  Specified using standardised joint names in FBXMotionToolkit.joint class. | 
| sampleTimes | Float List  | A list of times in seconds.                                                                                  | 

Example:
```
# Loads then conforms motion data before extracting joint data as global positions.
import FBXMotionToolkit as fmt

motion1 = fmt.importFBXSequence(r'C:\motionFile1.fbx')
motion1.mapJoints(r'C:\jointMapFile.csv')
duration1 = motion1.getTimeOfLastKey(fmt.joint.root, fmt.animationCurveType.ROTATION, fmt.axis.x)

jointList = [fmt.joint.rhip, fmt.joint.lhip]
motion1.makeJointsAnimatable(jointList, fmt.animationCurveType.ROTATION)
timePoints = motion1.getJointKeyTimes(fmt.joint.rhip, fmt.animationCurveType.ROTATION, fmt.axis.x)
jointGlobalPositions = motion1.getJointAsGlobalTranslations(jointList, timePoints)
```

### getJointAsRelativeTranslations

> jointDataRelativeTranslations FBXSequence.getJointAsRelativeTranslations(jointList, baseJoint, sampleTimes)

Retrieves the rotation data for a single joint or list of joints as positions specified in the local coordinate space of a base joint, returning the joint positions for each joint for every time point specified in sampleTimes.  All positional data is returned in a single joint data object, which allows easier access and analysis of joint data.

All joints must be animatable with key frames at matching times on all joint axis.  Use FBXSequence.makeJointAnimatable() and FBXSequence.resample() to make joints conform to one another.

Parameters:

| Name        | Data Type   | Description                                                                                                  |
|-------------|-------------|--------------------------------------------------------------------------------------------------------------|
| jointList   | String List | A single joint or list of joints.  Specified using standardised joint names in FBXMotionToolkit.joint class. | 
| baseJoint   | String      | A single joint.  Specified using standardised joint names in FBXMotionToolkit.joint class.                   | 
| sampleTimes | Float List  | A list of times in seconds.                                                                                  | 

Example:
```
# Loads then conforms motion data before extracting joint data as positions within the root joints coordinate space.
import FBXMotionToolkit as fmt

motion1 = fmt.importFBXSequence(r'C:\motionFile1.fbx')
motion1.mapJoints(r'C:\jointMapFile.csv')
duration1 = motion1.getTimeOfLastKey(fmt.joint.root, fmt.animationCurveType.ROTATION, fmt.axis.x)

jointList = [fmt.joint.rhip, fmt.joint.lhip]
motion1.makeJointsAnimatable(jointList, fmt.animationCurveType.ROTATION)
timePoints = motion1.getJointKeyTimes(fmt.joint.rhip, fmt.animationCurveType.ROTATION, fmt.axis.x)
jointRelative = motion1.getJointAsRelativeTranslations(jointList, fmt.joint.root, timePoints)
```