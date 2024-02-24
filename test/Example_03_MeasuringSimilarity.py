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

# measure similarity using correlation based metric
jointQ1flat = jointQ1.getFlatJointData()
jointQ2flat = jointQ2.getFlatJointData()
c = fmt.st.measureCorrelationSimilarity(jointQ1flat, jointQ2flat, fmt.st.CorrelationMethod.Pearson)
