import numpy as np
import FBXMotionToolkit as fmt
import scipy.stats as stats

# Specify paths to fbx motion file and joint map file
sampleDataFolder = r'C:\Users\mathew.randall\OneDrive - Birmingham City University\FBXMotionToolkit\TestData\\'
motionFile = sampleDataFolder + "alined_walk_01.fbx"
motionFile2 = sampleDataFolder + "alined_walk_02.fbx"

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

print("seq1: " + str(seq1Duration))
print("seq2: " + str(seq2Duration))

#seq.unrollAllJoints()
seq.resample(120, seq1Duration)
seq2.resample(120, seq2Duration)

seq.export(sampleDataFolder + "resample.fbx")

jointList = [fmt.joint.rhip, fmt.joint.lhip, fmt.joint.rknee, fmt.joint.lknee, fmt.joint.rshoulder, fmt.joint.lshoulder, fmt.joint.lelbow, fmt.joint.relbow]
#jointList = [fmt.joint.rhip, fmt.joint.lhip, fmt.joint.rknee]

jointQuats = seq.getJointRotationAsQuaternions(jointList)
jointQuats2 = seq2.getJointRotationAsQuaternions(jointList)

print(jointQuats2.getFrameCount())
print(jointQuats.getFrameCount())

tw = fmt.timewarp(jointQuats, jointQuats2)
tw.graphTimewarp()
seq.applyTimewarp(tw.DTWremap)

jointEulers = seq.getJointRotationAsEulers(jointList)
jointEulers2 = seq2.getJointRotationAsEulers(jointList)

seq.export(sampleDataFolder + "aligned.fbx")

c = fmt.st.measureCorrelationSimilarity(jointEulers.getFlatJointData(), jointEulers2.getFlatJointData(), fmt.st.CorrelationMethod.Pearson)
print(c)


'''
sampleTimes = seq.getJointKeyTimes(fmt.joint.rhip, fmt.animationCurveType.ROTATION, fmt.axis.x)
jointQuats = seq.getJointRotationAsQuaternions(jointList)
jointQuats2 = seq2.getJointRotationAsQuaternions(jointList)

#speed1 = jointQuats.getJointVectorsAsSpeed()
#speed2 = jointQuats2.getJointVectorsAsSpeed()

print("input duration: " + str(jointQuats.getFrameCount()))
print("target duration: " + str(jointQuats2.getFrameCount()))

#d = fmt.st.measureSimilarity(jointQuats, jointQuats2)
#print(d)

tw = fmt.timewarp(jointQuats, jointQuats2)
tw.graphTimewarp()
seq.applyTimewarp(tw.DTWremap)



# remove sequence from memory.
seq.destroy()
seq2.destroy()
'''