## Object Initialisation
A FBXSequence object is created by calling the importFBXSequence() function.
### ImportFBXSequence
> void **FBXSequence** = **ImportFBXSequence**(string **FilePath**)

Opens and loads the FBX file specified in the FilePath, then returns a FBXSequence object that allows the FBX data and file to be read, manipulated and exported.

**Parameters**

| Name | Data Type | Description |
| --- | --- | --- |
| FilePath | String | Path locating the FBX file to be imported |

**Example**
```
myFBX = seq = FBXMotionToolkit.importFBXSequence(r'C:\motionFile.fbx')
```
## Creating a Joint Map ##

> void **FBXSequence.ImportFBXSequence**(string **JointMapFilePath**)

To allow an FBXSequence object to correctly access joints within an FBX file, a .csv joint map file must be created and loaded into the FBXSequence object.  The joint map file maps the names of the joints within the FBX file, to a standard set of joints names.  

The example below shows a .csv file mapping a joint to each standardised joints names. Each row consists of <standardised FBXSequence jointname>, <jointname within fbx file>.  An example joint map file can be seen in the test folder.

The standardised joint names are enumerated in the FBXMotionToolkit.joint class.  The names of the joints within the files can be found by opening the FBX file in a DCC package or by using the the FBXSequence.PrintSceneHierarchy() function.

```
root,Hips
rhip,RightUpLeg
rknee,RightLeg
rankle,RightFoot
rtoes,RightToeBase
lhip,LeftUpLeg
lknee,LeftLeg
lankle,LeftFoot
ltoes,LeftToeBase
rshoulder,RightArm
relbow,RightForeArm
rwrist,RightHand
lshoulder,LeftArm
lelbow,LeftForeArm
lwrist,LeftHand
head,Head
neck,Neck
chest,Spine3
belly,Spine1
```
**Parameters**

| Name | Data Type | Description |
| --- | --- | --- |
| JointMapFilePath | String | Path locating the .csv joint map file |
