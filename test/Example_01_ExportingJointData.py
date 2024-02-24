# Open motion
import FBXMotionToolkit as fmt

# Fill in missing keyframes
joints = [fmt.joint.rhip, fmt.joint.lhip]
motion = fmt.importFBXSequence("Dance.fbx")
motion.mapJoints("jointMap.csv")

# Convert and extract joint data
jointQ = motion.getJointRotationAsQuaternions(joints)
jointQ.exportJointDataCSV("jointData.csv")