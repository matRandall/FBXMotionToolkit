import FBXMotionToolkit as fmt

# Open motion
joints = [fmt.joint.relbow, fmt.joint.rknee]
motion = fmt.importFBXSequence("Dance.fbx")
motion.mapJoints("jointMap.csv")

# Fill in missing keyframes
motionDuration = motion.getTimeOfLastKey(fmt.joint.root, fmt.animationCurveType.ROTATION, fmt.axis.x)
motion.makeJointsAnimatable(joints, fmt.animationCurveType.ROTATION)
motion.unrollAllJoints()
motion.resample(120, motionDuration)

# Convert and extract joint data
jointQ = motion.getJointRotationAsQuaternions(joints)
jointQ.exportJointDataCSV("jointData.csv")

# Export FBX file
motion.export("myFBX.fbx")

# Graph the joint Eulers
jointQ = motion.getJointRotationAsEulers(joints)
jointQ.plotJointData(fmt.joint.rknee)