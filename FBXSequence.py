import fbx
import sys
import csv
import os
import FBXMotionToolkit

class FBXSequence():

    # constuctor
    def __init__(self, motionFile):

        # initialise properties
        self.file = motionFile
        self.jointMap = {}
        self.jointNameMap = {}
        self.animStackIndex = 0
        self.animLayerIndex = 0

        # create empty FBX scene
        self.fbxManager = fbx.FbxManager.Create()

        # import motion file
        self.fbxImporter = fbx.FbxImporter.Create(self.fbxManager, 'theImporter')
        self.importStatus = self.fbxImporter.Initialize(self.file)

        # check the import status before moving on - exit if needed
        if self.importStatus == False:
            print("FBX import failed check file name")
            sys.exit()

        # if status is good create a new scene form the imported scene
        self.scene = fbx.FbxScene.Create(self.fbxManager, 'theScene')
        self.fbxImporter.Import(self.scene)
        self.fbxImporter.Destroy() # destroy importer once imported.
        self.rootNode = self.scene.GetRootNode()
        self.eval = self.scene.GetAnimationEvaluator()

        # get the first animation stack and animation layer
        lAnimStack = self.scene.GetSrcObject(fbx.FbxCriteria().ObjectType(fbx.FbxAnimStack.ClassId),
                                             self.animStackIndex)
        self.animLayer = lAnimStack.GetMember(fbx.FbxCriteria().ObjectType(fbx.FbxAnimLayer.ClassId),
                                          self.animLayerIndex)

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
        self.jointMap.clear()

        # go through each joint in nanme map calling function to find joint
        for joint in self.jointNameMap:
            searchName = self.jointNameMap[joint]
            theNode = self.checkNodeNameMatch(self.rootNode, searchName)
            self.jointMap[joint] = theNode

    # Checks if the joint map exists
    def checkJointMapExists(self):
        if len(self.jointMap) == 0:
            print("joints haven't been mapped, programme stopped")
            print("use mapJoints to create a jointMap")
            sys.exit()
            return False
        else:
            return True

    # recursive function that finds the node with a name ending with a string matching the searchString.
    def checkNodeNameMatch(self, node, searchString):
        searchChild = False
        theNodeName = node.GetName()
        # check if searchString exists on the end of the joint name
        if len(searchString) <= len(theNodeName):
            if (searchString == theNodeName[-len(searchString):]):
                return node

        # if not match then continue function to look at children
        for i in range(node.GetChildCount()):
            nodeTest = self.checkNodeNameMatch(node.GetChild(i), searchString)
            if nodeTest is not None:
                return nodeTest

    def getAllChildren(self, node):
        nodeList = []
        for i in range(node.GetChildCount()):
            childNode = node.GetChild(i)
            nodeList.append(childNode)
            nodeList += self.getAllChildren(childNode)
        return nodeList

    # Get the time of the last keyframe in a specified animation curve, based on specfified joint, animation curve type ("rotation" or "translation") and axis.
    def getTimeOfLastKey(self, joint, animationType, axis):

        # check if joints exist
        self.checkJointMapExists()

        # get the animation curve
        curves = self.getJointAnimCurves(joint, animationType)

        # get the time of the last key frame in the animation curve
        lastFrameTime = curves[axis].KeyGet(self.getNumberKeyframes(joint, animationType, axis) - 1).GetTime().GetSecondDouble()

        return lastFrameTime

    # Gets the number of keyframes in a specified animation curve, based on specfified joint, animation curve type ("rotation" or "translation") and axis
    def getNumberKeyframes(self, joint, animationType, axis):

        # check if joints exist
        self.checkJointMapExists()

        # get the animation stack (take), then animation layer in stack, then animation curve in animation layer
        lCurves = self.getJointAnimCurves(joint, animationType)

        # return the number of keys in the first animation curve
        return lCurves[axis].KeyGetCount()

    # Gets the animation curves for a specified joint and animation curve type ("rotation" or "translation")
    def getJointAnimCurves(self, joint, animationType):

        # check if joints exist
        self.checkJointMapExists()

        # create empty list to store XYZ animation curves
        lcurves = []


        # if translation then get the translation nodes
        if animationType == "translation":
            lcurves.append(self.jointMap[joint].LclTranslation.GetCurve(self.animLayer, "X", False))
            lcurves.append(self.jointMap[joint].LclTranslation.GetCurve(self.animLayer, "Y", False))
            lcurves.append(self.jointMap[joint].LclTranslation.GetCurve(self.animLayer, "Z", False))

        # if translation then get the rotation nodes
        elif animationType == "rotation":
            lcurves.append(self.jointMap[joint].LclRotation.GetCurve(self.animLayer, "X", False))
            lcurves.append(self.jointMap[joint].LclRotation.GetCurve(self.animLayer, "Y", False))
            lcurves.append(self.jointMap[joint].LclRotation.GetCurve(self.animLayer, "Z", False))

        # return the list of curves
        return lcurves

    # function resamples all the curves in a motion using specified frame rate, up to a given time limit specified in seconds.  Any frames beyond the time limit will be lost.
    def resample(self, fps, timeLimit):

        # need to get totalTime at the start so that all curves confirm to the same standard.
        #originalFPS = self.getFramesPerSecond()
        totalTime = timeLimit
        totalFrames = int(round(totalTime * fps) + 1)

        # create a list of all the joints in sequence
        motionRoot = self.jointMap["root"]
        nodeList = [motionRoot]
        nodeList += self.getAllChildren(motionRoot)

        # set up a list of axis
        axis = ["X", "Y", "Z"]

        # resample of the frame in every joint
        for node in nodeList:

            # resample the translation curves
            for ax in axis:
                curve = node.LclTranslation.GetCurve(self.animLayer, ax, False)
                if curve != None:
                    self.resampleCurve(curve, fps, totalFrames)

            # resample the rotation curves
            for ax in axis:
                curve = node.LclRotation.GetCurve(self.animLayer, ax, False)
                if curve != None:
                    #print(node.GetName() + ": Translation")
                    self.resampleCurve(curve, fps, totalFrames)

    # resmaples an animation curve to a given frame rate and time limit
    def resampleCurve(self, input, fps, totalFrames):

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

    def export(self, fullpath):
        exporter = fbx.FbxExporter.Create(self.fbxManager, '')
        exporter.Initialize(fullpath)
        exporter.Export(self.scene)
        exporter.Destroy()
