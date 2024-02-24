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

'''
# Perform DTW Alignment
tw = fmt.Timewarp(jointQ1, jointQ2)
tw.graphTimewarp()
motion1.applyTimewarp(tw.DTWremap)
motion1.export("aligned.fbx")
'''

# Destroy Motions
motion1.destroy()
motion2.destroy()