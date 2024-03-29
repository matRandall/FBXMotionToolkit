import fbx
import sys
import csv
import os
import JointDataClasses as jc
from scipy.spatial.transform import Rotation as R
import numpy as np
import FBXMotionToolkit as fmt

class FBXSequence():

    # constuctor
    def __init__(self, motionFile):

        # initialise public properties
        self.file = motionFile
        self.jointNameMap = {}
        
        # initialise private properties
        self.__jointMap = {}
        self.__animStackIndex = 0
        self.__animLayerIndex = 0

        # create empty FBX scene
        self.fbxManager = fbx.FbxManager.Create()

        # import motion file
        self.__fbxImporter = fbx.FbxImporter.Create(self.fbxManager, 'theImporter')
        self.__importStatus = self.__fbxImporter.Initialize(self.file)

        # check the import status before moving on - exit if needed
        if self.__importStatus == False:
            print("FBX import failed check file name")
            sys.exit()

        # if status is good create a new scene form the imported scene
        self.scene = fbx.FbxScene.Create(self.fbxManager, 'theScene')
        self.__fbxImporter.Import(self.scene)
        self.__fbxImporter.Destroy() # destroy importer once imported.
        self.__rootNode = self.scene.GetRootNode()
        self.__eval = self.scene.GetAnimationEvaluator()

        # get the first animation stack and animation layer
        self.__animStack = self.scene.GetSrcObject(fbx.FbxCriteria().ObjectType(fbx.FbxAnimStack.ClassId),
                                             self.__animStackIndex)
        self.__animLayer = self.__animStack.GetMember(fbx.FbxCriteria().ObjectType(fbx.FbxAnimLayer.ClassId),
                                          self.__animLayerIndex)

    def destroy(self):
        self.fbxManager.Destroy()
        # function maps nodes to standard names using a joint map

    def mapJoints(self, map):

        # clear then read in the joint name map
        self.jointNameMap.clear()

        # check file exists
        if os.path.exists(map) == False:
            print("Joint map file specified doesn't exist")
            sys.exit()

        # reading mapping of joint names from CSV file
        with open(map) as mapfile:
            mapReader = csv.reader(mapfile, csv.excel)
            for row in mapReader:
                self.jointNameMap[row[0]] = row[1]

        # clear the current joint map
        self.__jointMap.clear()

        # go through each joint in nanme map calling function to find joint
        for joint in self.jointNameMap:
            searchName = self.jointNameMap[joint]
            theNode = self.__checkNodeNameMatch(self.__rootNode, searchName)
            self.__jointMap[joint] = theNode

    # Checks if the joint map exists
    def __checkJointMapExists(self):
        if len(self.__jointMap) == 0:
            print("joints haven't been mapped, programme stopped")
            print("use mapJoints to create a jointMap")
            sys.exit()
            return False
        else:
            return True

    # recursive function that finds the node with a name ending with a string matching the searchString.
    def __checkNodeNameMatch(self, node, searchString):
        searchChild = False
        theNodeName = node.GetName()
        # check if searchString exists on the end of the joint name
        if len(searchString) <= len(theNodeName):
            if (searchString == theNodeName[-len(searchString):]):
                return node

        # if not match then continue function to look at children
        for i in range(node.GetChildCount()):
            nodeTest = self.__checkNodeNameMatch(node.GetChild(i), searchString)
            if nodeTest is not None:
                return nodeTest

    def __isJointAnimated(self, joint, animationType):

        node = self.__jointMap[joint]
        isAnimated = True

        for axis in ["X", "Y", "Z"]:
            if animationType == fmt.animationCurveType.ROTATION:
                if node.LclRotation.GetCurve(self.__animLayer, axis, False) == None:
                    isAnimated = False
            elif animationType == fmt.animationCurveType.TRANSLATION:
                if node.LclTranslation.GetCurve(self.__animLayer, axis, False) == None:
                    isAnimated = False

        return isAnimated

    def __checkIfAnimated(self, joint, animationType):

        if self.__isJointAnimated(joint, animationType) == False:
            print(
                "Joint is not animated. Joint must have animation curve to get joint global position. Use makeJointAnimatable() function to carete animation curves")
            sys.exit()

    def __getAllChildren(self, node):
        nodeList = []
        for i in range(node.GetChildCount()):
            childNode = node.GetChild(i)
            nodeList.append(childNode)
            nodeList += self.__getAllChildren(childNode)
        return nodeList

    # Get the time of the last keyframe in a specified animation curve, based on specfified joint, animation curve type ("rotation" or "translation") and axis.
    def getTimeOfLastKey(self, joint, animationType, axis):

        # check if joints exist
        self.__checkJointMapExists()

        # get the animation curve
        curves = self.__getJointAnimCurves(joint, animationType)

        # get the time of the last key frame in the animation curve
        lastFrameTime = curves[axis].KeyGet(self.getNumberKeyframes(joint, animationType, axis) - 1).GetTime().GetSecondDouble()

        return lastFrameTime
    def getJointKeyTimes(self, joint, animationType, axis):

        node = self.__jointMap[joint]

        axisLabels = ["X", "Y", "Z"]
        axisIndex = axisLabels[axis]

        # check if the curve is animated
        curveIsAnimated = True
        if animationType == fmt.animationCurveType.ROTATION:
            if node.LclRotation.GetCurve(self.__animLayer, axisIndex, False) == None:
                curveIsAnimated = False
        elif animationType == fmt.animationCurveType.TRANSLATION:
            if node.LclTranslation.GetCurve(self.__animLayer, axisIndex, False) == None:
                curveIsAnimated = False
        if curveIsAnimated == False:
            print(
                "Joint is not animated. Joint must have animation curve to get joint global position. Use makeJointAnimatable() function to carete animation curves")
            sys.exit()

        # get time point for each ketframe in the animation curve
        timeCurve = self.__getJointAnimCurves(joint, animationType)[axis]
        times = []
        for f in range(timeCurve.KeyGetCount()):
            time = timeCurve.KeyGet(f).GetTime()
            times.append(time.GetSecondDouble())

        return times

    # Gets the number of keyframes in a specified animation curve, based on specfified joint, animation curve type ("rotation" or "translation") and axis
    def getNumberKeyframes(self, joint, animationType, axis):

        # check if joints exist
        self.__checkJointMapExists()

        # get the animation stack (take), then animation layer in stack, then animation curve in animation layer
        lCurves = self.__getJointAnimCurves(joint, animationType)

        # return the number of keys in the first animation curve
        return lCurves[axis].KeyGetCount()

    def getFramesPerSecond(self, joint, animationType, axis):

        curves = self.__getJointAnimCurves(joint, animationType)[axis]
        t1 = curves.KeyGet(0).GetTime()
        t2 = curves.KeyGet(1).GetTime()
        fTime = t2 - t1
        fTimeSec = fTime.GetSecondDouble()
        fps = round(1. / fTimeSec)

        return fps

    # Gets the animation curves for a specified joint and animation curve type ("rotation" or "translation")
    def __getJointAnimCurves(self, joint, animationType):

        # check if joints exist
        self.__checkJointMapExists()

        # create empty list to store XYZ animation curves
        lcurves = []


        # if translation then get the translation nodes
        if animationType == "translation":
            lcurves.append(self.__jointMap[joint].LclTranslation.GetCurve(self.__animLayer, "X", False))
            lcurves.append(self.__jointMap[joint].LclTranslation.GetCurve(self.__animLayer, "Y", False))
            lcurves.append(self.__jointMap[joint].LclTranslation.GetCurve(self.__animLayer, "Z", False))

        # if translation then get the rotation nodes
        elif animationType == "rotation":
            lcurves.append(self.__jointMap[joint].LclRotation.GetCurve(self.__animLayer, "X", False))
            lcurves.append(self.__jointMap[joint].LclRotation.GetCurve(self.__animLayer, "Y", False))
            lcurves.append(self.__jointMap[joint].LclRotation.GetCurve(self.__animLayer, "Z", False))

        # return the list of curves
        return lcurves

    # this function extracts the motion curves for a set of joints into a eular joint data class
    def getJointRotationAsEulers(self, jointList):

        if type(jointList) == type("string"):
            jointList = [jointList]

        # create empty list of curves
        curves = []

        # go through each joint
        for joint in jointList:
            #get animation curves for joint

            jointCurves = self.__getJointAnimCurves(joint, "rotation")

            if jointCurves != None:

                # empty list of axes curves
                axisCurves = []

                # go through the curve of each axis (x,y,z)
                for axis in range(3):

                    if jointCurves[axis] != None:

                        # craete empty list of samples
                        samples = []

                        # go through each key in curve
                        for frame in range(jointCurves[axis].KeyGetCount()):

                            # get the key value and add it ot the sample list
                            samples.append(jointCurves[axis].KeyGet(frame).GetValue())

                        # add the list of smaples to the curve list
                        axisCurves.append(samples)

                curves.append(axisCurves)

        axes = ["x", "y", "z"]
        jointData = jc.JointDataEulers(jointList, axes, curves)

        return jointData

    def getJointRotationAsQuaternions(self, jointList):

        if type(jointList) == type("string"):
            jointList = [jointList]

        eulerData = self.getJointRotationAsEulers(jointList)
        QuaternionData = np.empty((len(jointList), 4, eulerData.getFrameCount()))
        axes = ["x", "y", "z", "w"]

        for j in range(len(jointList)):

            joint = jointList[j]
            jointRotationOrder = self.getRotationOrder(joint)

            jointEulerData = eulerData.getJointData(joint)
            jointRotationData = R.from_euler(jointRotationOrder, jointEulerData.transpose(), degrees=True)
            jointQuaternionData = jointRotationData.as_quat(canonical=True).transpose()

            QuaternionData[j] = jointQuaternionData

        jointData = jc.JointDataQuaternions(jointList, axes, QuaternionData)

        return jointData

    def getJointRotationAsMatrices(self, jointList):

        if type(jointList) == type("string"):
            jointList = [jointList]

        eulerData = self.getJointRotationAsEulers(jointList)
        MartrixData = np.empty((len(jointList), 9, eulerData.getFrameCount()))
        axes = ["m00", "m01", "m02", "m10", "m11", "m12", "m20", "m21", "m22"]

        for j in range(len(jointList)):
            joint = jointList[j]
            jointRotationOrder = self.getRotationOrder(joint)

            jointEulerData = eulerData.getJointData(joint)
            jointRotationData = R.from_euler(jointRotationOrder, jointEulerData.transpose(), degrees=True)
            jointMatrixData = jointRotationData.as_matrix().transpose()

            stackedMatrix = np.stack((jointMatrixData[0,0], jointMatrixData[0,1], jointMatrixData[0,2],
                                      jointMatrixData[1,0], jointMatrixData[1,1], jointMatrixData[1,2],
                                      jointMatrixData[2,0], jointMatrixData[2,1], jointMatrixData[2,2]))

            MartrixData[j] = stackedMatrix

            jointData = jc.JointDataMatrices(jointList, axes, MartrixData)

            return jointData

    def getJointRotationAsDisplacementVectors(self, jointList):

        if type(jointList) == type("string"):
            jointList = [jointList]

        axes = ["x", "y", "z"]

        # create empty list of curves
        curves = []

        # get the times of the keys
        timeCurve = self.__getJointAnimCurves(jointList[0], fmt.animationCurveType.ROTATION)[0]
        times = []
        for f in range(timeCurve.KeyGetCount()):
            time = timeCurve.KeyGet(f).GetTime()
            times.append(time)

        for j in jointList:
            node = self.__jointMap[j]
            x = []
            y = []
            z = []
            for t in range(len(times)):
                matrix = node.EvaluateLocalTransform(times[t])

                RMatrix = fbx.FbxAMatrix()
                RMatrix.SetR(matrix.GetR())

                IDVector = fbx.FbxVector4(0, 1, 0, 1)
                vVector = RMatrix.MultT(IDVector)

                x.append(vVector[0])
                y.append(vVector[1])
                z.append(vVector[2])

            jointAxes = [x,y,z]
            curves.append(jointAxes)

        jointData = jc.JointDataDisplacementVectors(jointList, axes, curves)

        return jointData

    # this function extracts global translations of a list of joint.
    # the global translation of each joint is sampled at the time of each key frame in the joint specified in the syncSampleJoint.
    def getJointAsGlobalTranslations(self, jointList, sampleTimes):

        if type(jointList) == type("string"):
            jointList = [jointList]

        axes = ["x", "y", "z"]

        # create empty list of curves
        curves = []

        for j in jointList:

            node = self.__jointMap[j]
            x = []
            y = []
            z = []
            for t in range(len(sampleTimes)):
                time = fbx.FbxTime()
                time.SetSecondDouble(sampleTimes[t])
                matrix = (node.EvaluateGlobalTransform(time))
                globalTranslation = matrix.GetT()

                x.append(globalTranslation[0])
                y.append(globalTranslation[1])
                z.append(globalTranslation[2])

            jointAxes = [x, y, z]
            curves.append(jointAxes)

        jointData = jc.JointDataGlobalTranslations(jointList, axes, curves)
        return jointData

    def getJointAsRelativeTranslations(self, jointList, baseJoint, sampleTimes):

        if type(jointList) == type("string"):
            jointList = [jointList]

        axes = ["x", "y", "z"]

        # create empty list of curves
        curves = []

        # get the reverse translation for the root
        baseNode = self.__jointMap[baseJoint]
        inverseBaseMatricies = []

        for t in sampleTimes:
            time = fbx.FbxTime()
            time.SetSecondDouble(t)
            baseMatrix = baseNode.EvaluateGlobalTransform(time)
            baseInverseMatrix = baseMatrix.Inverse()
            inverseBaseMatricies.append(baseInverseMatrix)

        # get the translations between the base joint and joint
        for j in jointList:

            node = self.__jointMap[j]
            x = []
            y = []
            z = []

            for timeIndex in range(len(sampleTimes)):
                time = fbx.FbxTime()
                time.SetSecondDouble(sampleTimes[timeIndex])

                jointMatrix = (node.EvaluateGlobalTransform(time))
                relativejointMatrix = inverseBaseMatricies[timeIndex] * jointMatrix
                relativeTranslation = relativejointMatrix.GetT()

                x.append(relativeTranslation[0])
                y.append(relativeTranslation[1])
                z.append(relativeTranslation[2])

            jointAxes = [x, y, z]
            curves.append(jointAxes)

        jointData = jc.JointDataRelativeTranslations(jointList, axes, curves, baseJoint)
        return jointData

    # function resamples all the curves in a motion using specified frame rate, up to a given time limit specified in seconds.  Any frames beyond the time limit will be lost.
    def resample(self, fps, timeLimit):

        # need to get totalTime at the start so that all curves confirm to the same standard.
        #originalFPS = self.getFramesPerSecond()
        totalTime = timeLimit
        totalFrames = int(round(totalTime * fps) + 1)

        # create a list of all the joints in sequence
        motionRoot = self.__jointMap["root"]
        nodeList = [motionRoot]
        nodeList += self.__getAllChildren(motionRoot)

        # set up a list of axis
        axis = ["X", "Y", "Z"]

        # resample of the frame in every joint
        for node in nodeList:

            # resample the translation curves
            for ax in axis:
                curve = node.LclTranslation.GetCurve(self.__animLayer, ax, False)
                if curve != None:
                    self.__resampleCurve(curve, fps, totalFrames)

            # resample the rotation curves
            for ax in axis:
                curve = node.LclRotation.GetCurve(self.__animLayer, ax, False)
                if curve != None:
                    self.__resampleCurve(curve, fps, totalFrames)

    # resmaples an animation curve to a given frame rate and time limit
    def __resampleCurve(self, input, fps, totalFrames):

        # create a new curve
        newCurve = fbx.FbxAnimCurve.Create(self.scene, "nCurve")

        # for each frame in the reference motion, sample the input motion, building a new curve
        for frame in range(totalFrames):

            # get the time of the new frame
            time = fbx.FbxTime()
            time.SetSecondDouble(frame * (1. / fps))

            # get the value of the curve at the time of the new frame
            value = input.Evaluate(time)

            # add a key to the new curve
            newKeyIndex = newCurve.KeyAdd(time)
            newCurve.KeySetValue(newKeyIndex[0], value[0])

        # copy all the keys from the new curve to the input curve, wiping existing keys.
        input.CopyFrom(newCurve, True)

    # perform universal timewarp of motion to a given duration in seconds by moving the key in each curve
    def UTW(self, currentDuration, newDuration, fps):

        # create a list of all the joints in sequence
        motionRoot = self.__jointMap[fmt.joint.root]
        nodeList = [motionRoot]
        nodeList += self.__getAllChildren(motionRoot)

        curveList = []
        axes = ["X", "Y", "Z"]

        for node in nodeList:
            for a in axes:

                tcurve = node.LclTranslation.GetCurve(self.__animLayer, a, False)
                if tcurve != None:
                    curveList.append(tcurve)

                rcurve = node.LclRotation.GetCurve(self.__animLayer, a, False)
                if rcurve != None:
                    curveList.append(rcurve)

        for animCurve in curveList:

            numKeys = animCurve.KeyGetCount()

            if(newDuration > currentDuration):
                for keyNum in range(numKeys - 1, -1, -1):
                    self.__retimeKey(animCurve, keyNum, newDuration, currentDuration)

            # if making it shorter go from first frame to last
            elif(newDuration < currentDuration):
                for keyNum in range(numKeys):
                    self.__retimeKey(animCurve, keyNum, newDuration, currentDuration)

        self.resample(fps, newDuration)

    # retime a key to fit a new motion duration
    def __retimeKey(self, animCurve, keyNum, targetDuration, oldDuration):

        #get the normalised postion of the frame in relation to the position of the last frame
        oldKeyTime = animCurve.KeyGet(keyNum).GetTime().GetSecondDouble()
        normalisedFramePos = oldKeyTime / oldDuration

        # calc new frame time
        frameTimeSec = normalisedFramePos * targetDuration

        # create time object with new time
        frameTime = fbx.FbxTime()
        frameTime.SetSecondDouble(frameTimeSec)

        # set the key frame to the new time
        keyVal = animCurve.KeyGet(keyNum).GetValue()
        animCurve.KeySet(keyNum, frameTime, keyVal)

    def applyTimewarp(self, frameMap):

        totalFramesOfOrginalMotion = self.getNumberKeyframes(fmt.joint.root, fmt.animationCurveType.ROTATION, fmt.axis.x)

        motionRoot = self.__jointMap["root"]
        nodeList = [motionRoot]
        nodeList += self.__getAllChildren(motionRoot)

        # get the first animation stack and animation layer
        lAnimStack = self.__animStack
        lAnimLayer = self.__animLayer

        # set up a list of axis
        axis = ["X", "Y", "Z"]

        # timewarp the rotation curves of each subsequent node
        for node in nodeList:
            for ax in axis:
                curve = node.LclRotation.GetCurve(lAnimLayer, ax, False)
                if curve != None:
                    if curve.KeyGetCount() == totalFramesOfOrginalMotion:
                        #print("rot" + node.GetName())
                        self.__DTWtimewarpCurve(curve, frameMap)
                curve = node.LclTranslation.GetCurve(lAnimLayer, ax, False)
                if curve != None:
                    if curve.KeyGetCount() == totalFramesOfOrginalMotion:
                        #print("trans" + node.GetName())
                        self.__DTWtimewarpCurve(curve, frameMap)

        # set the timespane of the take
        startTime = fbx.FbxTime()
        startTime.SetSecondDouble(0.)

        endTime = fbx.FbxTime()
        endTime.SetSecondDouble(self.getTimeOfLastKey(fmt.joint.root, fmt.animationCurveType.ROTATION, fmt.axis.x))

        timeSpan = fbx.FbxTimeSpan(startTime, endTime)

        lAnimStack.SetLocalTimeSpan(timeSpan)
        lAnimStack.SetReferenceTimeSpan(timeSpan)

    # applies a timewarp to a curve using DTWmap
    def __DTWtimewarpCurve(self, curve, DTWmap):

        fps = self.getFramesPerSecond(fmt.joint.root, fmt.animationCurveType.ROTATION, fmt.axis.x)
        frameInterval = 1. / float(fps)

        time = 0.

        # save unwarped values of the curve
        oldCurveValues = []
        for i in range(curve.KeyGetCount()):
            oldCurveValues.append(curve.KeyGet(i).GetValue())

        # wipe the keys on the curve
        curve.KeyClear()

        # write the old values fo the curve back to the curve using the warp.
        for i in range(len(DTWmap)):
            newValue = oldCurveValues[DTWmap[i]]

            newTime = fbx.FbxTime()
            newTime.SetSecondDouble(time)

            newKeyIndex = curve.KeyAdd(newTime)
            curve.KeySetValue(newKeyIndex[0], newValue)

            time += frameInterval

    def unrollJointAxis(self, joint, axis):
        curve = self.__getJointAnimCurves(joint, fmt.animationCurveType.ROTATION)[axis]
        self.__unrollCurves([curve])

    def unrollJoint(self, joint):
        curves = self.__getJointAnimCurves(joint, fmt.animationCurveType.ROTATION)
        self.__unrollCurves(curves)

    def unrollAllJoints(self):
        curves = []

        # create a list of all the joints in sequence
        motionRoot = self.__jointMap["root"]
        nodeList = [motionRoot]
        nodeList += self.__getAllChildren(motionRoot)

        # set up a list of axis
        axis = ["X", "Y", "Z"]

        for node in nodeList:
            for ax in axis:
                rCurve = node.LclRotation.GetCurve(self.__animLayer, ax, False)
                if rCurve != None:
                    curves.append(rCurve)
        self.__unrollCurves(curves)

    def __unrollCurves(self, curves):

        threshold = 340

        for curve in curves:
            increment = 0
            keyCount = curve.KeyGetCount()
            for key in range(1, keyCount):
                lastkeyVal = curve.KeyGetValue(key - 1)
                keyVal = curve.KeyGetValue(key)
                keyVal += increment
                dif = keyVal - lastkeyVal
                if dif > threshold:
                    increment -= 360
                    keyVal -= 360
                if dif < -threshold:
                    increment += 360
                    keyVal += 360
                curve.KeySetValue(key, keyVal)



    def makeJointsAnimatable(self, jointList, animationType):

        # check if joints exist
        self.__checkJointMapExists()

        if type(jointList) == type("string"):
            jointList = [jointList]

        for joint in jointList:
            node = self.__jointMap[joint]

            for axis in ["X", "Y", "Z"]:
                node.LclRotation.GetCurve(self.__animLayer, axis, True)

    # save the scene as a .fbx file.
    def export(self, fullpath):
        exporter = fbx.FbxExporter.Create(self.fbxManager, '')
        exporter.Initialize(fullpath)
        exporter.Export(self.scene)
        exporter.Destroy()

    # print a hierarchical display of the nodes along with ley information each node.
    def printSceneHierarchy(self):
        sceneRoot = self.scene.GetRootNode()

        for i in range(sceneRoot.GetChildCount()):
            self.__printNodeName(sceneRoot.GetChild(i), 0)

    def __printNodeName(self, node, depth):
        # start text with an indend position of node in hierarchy
        text = ""
        for i in range(depth):
            text += "   "

        # add the name of the node
        text += node.GetName()

        print(text)

        # search recursively for child nodes
        for i in range(node.GetChildCount()):
            self.__printNodeName(node.GetChild(i), depth + 1)

    def exportJointInfo(self, outputFile):

        header = ["Mapped Name", "FBX Name", "Rotation Order", "TX Key Count", "TY Key Count", "TZ Key Count", "RX Key Count", "RY Key Count", "RZ Key Count", "Time of Last Key (secs)"]
        data = []

        for j in self.__jointMap.keys():
            row = [j]
            row.append(self.jointNameMap[j])

            jointNode = self.__jointMap[j]
            timeOfLastLey = 0

            rotationOrder = self.getRotationOrder(j)
            row.append(rotationOrder)

            axis = ["X", "Y", "Z"]

            # loop through each axis getting information on translation animation keyframes
            for ax in axis:
                nodeCurve = jointNode.LclTranslation.GetCurve(self.__animLayer, ax, False)
                if nodeCurve != None:
                    numKeys = nodeCurve.KeyGetCount()
                    axisLastKeyframeTime = nodeCurve.KeyGet(numKeys - 1).GetTime().GetSecondDouble()
                    if axisLastKeyframeTime > timeOfLastLey:
                        timeOfLastLey = axisLastKeyframeTime
                else:
                    numKeys = 0
                row.append(str(numKeys))

            # loop through each axis getting information on rotational animation keyframes
            for ax in axis:
                nodeCurve = jointNode.LclRotation.GetCurve(self.__animLayer, ax, False)
                if nodeCurve != None:
                    numKeys = nodeCurve.KeyGetCount()
                    axisLastKeyframeTime = nodeCurve.KeyGet(numKeys - 1).GetTime().GetSecondDouble()
                    if axisLastKeyframeTime > timeOfLastLey:
                        timeOfLastLey = axisLastKeyframeTime
                else:
                    numKeys = 0
                row.append(str(numKeys))

            row.append(timeOfLastLey)
            data.append(row)

        fmt.writeDataToCSV(outputFile, data, header)

    #returns the order in which joint rotaitons are being applied in a form that can be used with SciPy
    def getRotationOrder(self, joint):

        theJoint = self.__jointMap[joint]
        fbxRotationOrder = theJoint.RotationOrder.Get()
        jointRotationOrder = "xyz"

        if jointRotationOrder == fbx.EFbxRotationOrder.eEulerXZY:
            jointRotationOrder = "xzy"
        elif jointRotationOrder == fbx.EFbxRotationOrder.eEulerYXZ:
            jointRotationOrder = "yxz"
        elif jointRotationOrder == fbx.EFbxRotationOrder.eEulerYZX:
            jointRotationOrder = "yzx"
        elif jointRotationOrder == fbx.EFbxRotationOrder.eEulerZXY:
            jointRotationOrder = "zxy"
        elif jointRotationOrder == fbx.EFbxRotationOrder.eEulerZYX:
            jointRotationOrder = "zyx"

        return jointRotationOrder
