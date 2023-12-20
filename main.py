import FBXMotionToolkit as fmt

# Load in sample data
sampleDataFolder = r'C:\Users\mathew.randall\OneDrive - Birmingham City University\FBXMotionToolkit\Toolkit\TestData\\'

testFile = sampleDataFolder + "aligned_walk_01.fbx"
jointMapFile = sampleDataFolder + "viconMap.csv"

seq = fmt.importFBXSequence(testFile)

seq.mapJoints(jointMapFile)


thetime = seq.getTimeOfLastKey(fmt.joint.belly, fmt.animationCurveType.ROTATION, fmt.axis.X)

print(thetime)

#seq.export(sampleDataFolder + "export.fbx")

seq.destroy()