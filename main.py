import numpy as np
import FBXMotionToolkit as fmt

# Specify paths to fbx motion file and joint map file
sampleDataFolder = r'C:\Users\mathew.randall\OneDrive - Birmingham City University\FBXMotionToolkit\Toolkit\TestData\\'
motionFile = sampleDataFolder + "aligned_walk_01.fbx"
motionFile2 = sampleDataFolder + "aligned_walk_02.fbx"

# Load the motion sequence, returning a reference.
seq = fmt.importFBXSequence(motionFile)
seq2 = fmt.importFBXSequence(motionFile2)

# Map joints in the motion to joint names defined within the toolkit, using the jointMapFile.
jointMapFile = sampleDataFolder + "viconMap.csv"
seq.mapJoints(jointMapFile)
seq2.mapJoints(jointMapFile)

# detime the end time of the motion based on the last key frame in the x-axis of the root joint.
seq1Duration = seq.getTimeOfLastKey(fmt.joint.root, fmt.animationCurveType.ROTATION, fmt.axis.x)
seq2Duration = seq2.getTimeOfLastKey(fmt.joint.root, fmt.animationCurveType.ROTATION, fmt.axis.x)

seq2.UTW(seq2Duration, seq1Duration)

# resample the entire motion at 30 frames per second
seq.resample(30, seq1Duration)
seq2.resample(30, seq1Duration)


jointList = [fmt.joint.rhip, fmt.joint.lhip]
'''
jointQuats = seq.getJointRotationAsQuaternions(jointList)
jointQuats2 = seq2.getJointRotationAsQuaternions(jointList)

c = jointQuats.getSimilarityMatixRotationalDistance(jointQuats2)
print(c)
'''


sampleTimes = seq.getJointKeyTimes(fmt.joint.rhip, fmt.animationCurveType.ROTATION, fmt.axis.x)
jointQuats = seq.getJointRotationAsDisplacementVectors(jointList)
jointQuats2 = seq2.getJointRotationAsDisplacementVectors(jointList)
d = jointQuats.measureSimilarity(jointQuats2)
print(d)
c = jointQuats.getSimilarityMatix(jointQuats2)
print(c)








# remove sequence from memory.
seq.destroy()
seq2.destroy()