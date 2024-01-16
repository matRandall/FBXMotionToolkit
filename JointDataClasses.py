import numpy as np
import FBXMotionToolkit as fmt
import matplotlib.pyplot as plt
import math
import JointDataClasses
import sys


class JointData():

    def __init__(self, joints, axisLabels, data):

        self.data = np.array(data)
        self.joints = joints
        self.axisLabels = axisLabels
        self.dataType = "type not specified"
        self.plotColors = ["r", "g", "b", "c", "m", "y", "tab:orange", "tab:brown", "k"]

    def getJointCount(self):
        return self.data.shape[0]

    def getAxisCount(self):
        return self.data.shape[1]

    def getFrameCount(self):
        return self.data.shape[2]

    # returns all the frame data for a given joint and axis as a numpy array
    def getJointAxisData(self, joint, axis):
        jointIndex = self.joints.index(joint)
        axisIndex = self.axisLabels.index(axis)
        data = np.array(self.data[jointIndex, axisIndex])
        return data

    # returns value of given joint axis on a given frame
    def getJointAxisFrameValue(self, joint, axis, frame):
        jointIndex = self.joints.index(joint)
        axisIndex = self.axisLabels.index(axis)
        value = np.array(self.data[jointIndex, axisIndex, frame])
        return value

    # returns all the axes values for a given joint on a given frame
    def getJointFrameData(self, joint, frame):
        jointIndex = self.joints.index(joint)
        data = np.array(self.data[jointIndex,:,frame])
        return data

    # returns all axes data for a given joint in a 2D array
    # shape (axes, frames)
    def getJointData(self, joint):
        jointIndex = self.joints.index(joint)
        data = np.array(self.data[jointIndex])
        return data

    def getFlatJointData(self):

        jointCount = self.data.shape[0]
        axisCount = self.data.shape[1]
        parameterCount = jointCount * axisCount

        flatJointData = np.empty((parameterCount, self.data.shape[2]))
        counter = 0

        for j in range(jointCount):
            for a in range(axisCount):
                axisValues = self.getJointAxisData(self.joints[j], a)
                flatJointData[counter] = axisValues
                counter += 1

        return flatJointData

    # function exports joint data to a csv file.
    def exportJointDataCSV(self, outputFile):

        jointCount = self.data.shape[0]
        axisCount = self.data.shape[1]
        frameCount = self.data.shape[2]

        header = []
        for j in range(jointCount):
            for a in range(axisCount):
                header.append(self.joints[j] + " : " + self.axisLabels[a])

        data = []
        for f in range(frameCount):
            datarow = []
            for j in range(jointCount):
                for a in range(axisCount):
                    value = float(self.getJointAxisFrameValue(self.joints[j], self.axisLabels[a], f))
                    datarow.append(value)
            data.append(datarow)

        fmt.writeDataToCSV(outputFile, data, header)

    def plotJointData(self, joint, **kwargs):

        jointIndex = self.joints.index(joint)
        plotTitle = kwargs.get("title", fmt.getJointTitle(joint) + " " + self.dataType)
        figureSize = kwargs.get("figureSize", (7,3))

        x = np.arange(0, self.getFrameCount())

        fig, ax = plt.subplots(figsize=figureSize)

        for a in range(self.getAxisCount()):

            ax.plot(x, self.data[jointIndex, a], c=self.plotColors[a])

        ax.set(xlabel='Frames', ylabel='Value', title=plotTitle)
        ax.legend(self.axisLabels, bbox_to_anchor =(1, 1))

        plt.tight_layout()
        plt.show()

    def checkMatchBetweenJointData(self, secondMotionJointData):

        motion1 = self
        motion2 = secondMotionJointData

        if motion1.getFrameCount() != motion2.getFrameCount():
            print("Error: The motion sequences do not have matching frame counts")
            return False

        if motion1.__class__.__name__ != motion2.__class__.__name__:
            print("Error: The motion sequences do not have matching data types")
            return False

        if motion1.joints != motion2.joints:
            print("Error: The motion sequences do have a matching set of joints")
            return False

        return True

# class inherits joint data to create a class for working with Euler joints
class JointDataEulers(JointData):

    def __init__(self, joints, axisLabels, data):
        JointData.__init__(self, joints, axisLabels, data)
        self.axes = vector3Axes()
        self.dataType = "Eulers"

# class inherits joint data to create a class for working with Quaternion joint data
class JointDataQuaternions(JointData):

    def __init__(self, joints, axisLabels, data):
        JointData.__init__(self, joints, axisLabels, data)
        self.axes = quaternionAxes()
        self.dataType = "Quaternions"

    # Function retrieves the distance between individual frames of specified joints.
    # Frames can be within the same motion sequence or from two different motion sequences.
    # If given multiple joints it will give you the sum of the difference of all the joints supplied
    def getRotationalDistanceBetweenFrames(self, jointList, firstMotionFrame, secondMotionJointData, secondMotionFrame):

        dist = 0.

        for joint in jointList:

            q1 = self.getJointFrameData(joint, firstMotionFrame)
            q2 = secondMotionJointData.getJointFrameData(joint, secondMotionFrame)

            dot = q1[0] * q2[0] + q1[1] * q2[1] + q1[2] * q2[2] + q1[3] * q2[3]

            if dot > 1:
                dot = 1

            d = (2 / math.pi) * math.acos(math.fabs(dot))

            dist += d

        return dist

    # Gets the rotational speed of the joints in degrees per frame as a joint data object with a single axis.
    def getJointsAsRotationalSpeed(self):

        jointSpeedData = []
        for j in range(self.getJointCount()):
            jointSpeedData.append([[]])

        for f in range(1, self.getFrameCount()):
            for j in range(self.getJointCount()):
                jointFrameSpeed = self.getRotationalDistanceBetweenFrames([self.joints[j]], f - 1, self, f)
                jointFrameSpeed = jointFrameSpeed * 180.
                jointSpeedData[j][0].append(jointFrameSpeed)

        axisLabels = ["deg/frame"]
        jointSpeedDataObj = JointDataClasses.JointDataRotationalSpeed(self.joints, axisLabels, jointSpeedData)
        return jointSpeedDataObj

    # Function returns the similarity of two motions base on rotational distance.
    # The total rotation distance between the two motions is divided by the joint multiplied frames
    def measureSimilarityRotationalDistance(self, secondMotionJointData):

        motion1 = self
        motion2 = secondMotionJointData

        if motion1.checkMatchBetweenJointData(motion2) == False:
            return None

        sum = 0

        for f in range(motion1.getFrameCount()):
            d = motion1.getRotationalDistanceBetweenFrames(motion1.joints, f, motion2, f)
            sum += d

        avgDist = sum / (motion1.getJointCount() * motion2.getFrameCount())

        return avgDist

    def getSimilarityMatixRotationalDistance(self, secondMotionJointData):

        motion1 = self
        motion2 = secondMotionJointData

        costMatrix = np.empty((motion1.getFrameCount(), motion2.getFrameCount()))

        cellCount = 0
        totalCells = motion1.getFrameCount() * motion2.getFrameCount()

        for f1 in range(motion1.getFrameCount()):
            for f2 in range(motion2.getFrameCount()):
                costMatrix[f1, f2] = motion1.getRotationalDistanceBetweenFrames(motion1.joints, f1, motion2, f2)
                cellCount += 1
                progress = int((cellCount / totalCells) * 100)
                sys.stdout.write("\rprogress: " + str(progress) + "%")
                sys.stdout.flush()

        print("\n")
        return costMatrix

# class inherits joint data to create a class containing Matrix joint data
class JointDataMatrices(JointData):

    def __init__(self, joints, axisLabels, data):
        JointData.__init__(self, joints, axisLabels, data)
        self.axes = matrixAxes()
        self.dataType = "Matrices"

    # returns all the axes values for a given joint on a given frame in the form a rotational matrix
    def getJointFrameDataAsMatrix(self, joint, frame):
        jointIndex = self.joints.index(joint)
        data = np.array(self.data[jointIndex,:,frame])

        rMatix = np.array([[data[0], data[1], data[2]],
                           [data[3], data[4], data[5]],
                           [data[6], data[7], data[8]]])

        return rMatix

    # returns all frames for a joint as a series of rotation matrices
    # shape (frames, 3, 3)
    def getJointDataAsMatrix(self, joint):

        jointMatrixData = np.empty((self.getFrameCount(), 3, 3))

        for f in range(self.getFrameCount()):
            jointMatrixData[f] = self.getJointFrameDataAsMatrix(joint, f)

        return jointMatrixData

# Class for add extra functionality specific to joints represented as vectors
class JointDataVectors(JointData):
    def __init__(self, joints, axisLabels, data):
        JointData.__init__(self, joints, axisLabels, data)

    # returns the distance between to motion frames as vector, relative to the first motion.
    def getDistanceBetweenFramesAsVector(self, joint, firstMotionFrame, secondMotionJointData, secondMotionFrame):

        v1 = self.getJointFrameData(joint, firstMotionFrame)
        v2 = secondMotionJointData.getJointFrameData(joint, secondMotionFrame)

        vDist = v2 - v1

        return vDist

    def getDifferenceBetweenFrames(self, jointList, firstMotionFrame, secondMotionJointData, secondMotionFrame):

        sumDiff = 0.

        for j in jointList:

            v1 = self.getJointFrameData(j, firstMotionFrame)
            v2 = secondMotionJointData.getJointFrameData(j, secondMotionFrame)

            vDist = v2 - v1
            dist = math.sqrt(math.fabs(vDist[0]) + math.fabs(vDist[1]) + math.fabs(vDist[2]))
            sumDiff += dist

        return sumDiff

    def getJointVectorsAsSpeed(self):

        jointSpeedData = []
        for j in range(self.getJointCount()):
            jointSpeedData.append([[]])

        for f in range(1, self.getFrameCount()):
            for j in range(self.getJointCount()):
                vDist = self.getDistanceBetweenFramesAsVector(self.joints[j], f - 1, self, f)
                dis = math.sqrt(math.fabs(vDist[0]) + math.fabs(vDist[1]) + math.fabs(vDist[2]))
                jointSpeedData[j][0].append(dis)

        axisLabels = ["$\Delta \Vert V \Vert$"]
        dataType = self.dataType + " Speed"
        jointSpeedDataObj = JointDataClasses.JointDataVectorSpeed(self.joints, axisLabels, jointSpeedData, dataType)
        return jointSpeedDataObj

    def getJointVectorsAsVelocityVectors(self):

        jointSpeedData = []
        for j in range(self.getJointCount()):
            jointSpeedData.append([[],[],[]])

        for f in range(1, self.getFrameCount()):
            for j in range(self.getJointCount()):
                vDist = self.getDistanceBetweenFramesAsVector(self.joints[j], f - 1, self, f)
                for a in range(3):
                    jointSpeedData[j][a].append(vDist[a])

        axisLabels = ["$\Delta x$", "$\Delta y$", "$\Delta z$"]
        dataType = self.dataType + " Velocity"
        jointSpeedDataObj = JointDataClasses.JointDataVectorVelocity(self.joints, axisLabels, jointSpeedData, dataType)
        return jointSpeedDataObj

    def measureSimilarity(self, secondMotionJointData):

        motion1 = self
        motion2 = secondMotionJointData

        if motion1.checkMatchBetweenJointData(motion2) == False:
            return None

        sum = 0

        for f in range(motion1.getFrameCount()):
            d = motion1.getDifferenceBetweenFrames(motion1.joints, f, motion2, f)
            sum += d

        avgDist = sum / (motion1.getJointCount() * motion2.getFrameCount())

        return avgDist

    def getSimilarityMatix(self, secondMotionJointData):

        motion1 = self
        motion2 = secondMotionJointData

        costMatrix = np.empty((motion1.getFrameCount(), motion2.getFrameCount()))

        cellCount = 0
        totalCells = motion1.getFrameCount() * motion2.getFrameCount()

        for f1 in range(motion1.getFrameCount()):
            for f2 in range(motion2.getFrameCount()):
                costMatrix[f1, f2] = motion1.getDifferenceBetweenFrames(motion1.joints, f1, motion2, f2)
                cellCount += 1
                progress = int((cellCount / totalCells) * 100)
                sys.stdout.write("\rprogress: " + str(progress) + "%")
                sys.stdout.flush()

        print("\n")
        return costMatrix

# class inherits joint data to create a class with joints parameterised as displacement vectors
class JointDataDisplacementVectors(JointDataVectors):

    def __init__(self, joints, axisLabels, data):
        JointData.__init__(self, joints, axisLabels, data)
        self.axes = vector3Axes()
        self.dataType = "Displacement Vector"

# class inherits joint data to create a class with joints parameterised as translations in global space
class JointDataGlobalTranslations(JointDataVectors):

    def __init__(self, joints, axisLabels, data):
        JointData.__init__(self, joints, axisLabels, data)
        self.axes = vector3Axes()
        self.dataType = "Global Translations"

# class inherits joint data to create a class with joints parameterised as translations in global space
class JointDataRelativeTranslations(JointDataVectors):

    def __init__(self, joints, axisLabels, data, baseJoint):
        JointData.__init__(self, joints, axisLabels, data)
        self.axes = vector3Axes()
        self.baseJoint = baseJoint
        baseJointName = fmt.getJointTitle(baseJoint)
        self.dataType = "Translations Relative to " + baseJointName

class JointDataSpeed(JointData):
    def __init__(self, joints, axisLabels, data):
        JointData.__init__(self, joints, axisLabels, data)

    def getDifferenceBetweenFrames(self, jointList, firstMotionFrame, secondMotionJointData, secondMotionFrame):

        sumDiff = 0.

        for j in jointList:

            s1 = self.getJointFrameData(j, firstMotionFrame)
            s2 = secondMotionJointData.getJointFrameData(j, secondMotionFrame)

            dif = math.fabs(s1[0] - s2[0])

            sumDiff += dif

        return sumDiff

    def measureSimilarity(self, secondMotionJointData):

        motion1 = self
        motion2 = secondMotionJointData

        if motion1.checkMatchBetweenJointData(motion2) == False:
            return None

        sum = 0

        for f in range(motion1.getFrameCount()):
            d = motion1.getDifferenceBetweenFrames(motion1.joints, f, motion2, f)
            sum += d

        avgDist = sum / (motion1.getJointCount() * motion2.getFrameCount())

        return avgDist

    def getSimilarityMatix(self, secondMotionJointData):

        motion1 = self
        motion2 = secondMotionJointData

        costMatrix = np.empty((motion1.getFrameCount(), motion2.getFrameCount()))

        cellCount = 0
        totalCells = motion1.getFrameCount() * motion2.getFrameCount()

        for f1 in range(motion1.getFrameCount()):
            for f2 in range(motion2.getFrameCount()):
                costMatrix[f1, f2] = motion1.getDifferenceBetweenFrames(motion1.joints, f1, motion2, f2)
                cellCount += 1
                progress = int((cellCount / totalCells) * 100)
                sys.stdout.write("\rprogress: " + str(progress) + "%")
                sys.stdout.flush()

        print("\n")
        return costMatrix

    def getJointsAsDifferentials(self):

        jointSpeedData = []
        for j in range(self.getJointCount()):
            jointSpeedData.append([[]])

        for f in range(1, self.getFrameCount()):
            for j in range(self.getJointCount()):
                jointFrameSpeed = self.getDifferenceBetweenFrames([self.joints[j]], f - 1, self, f)
                jointSpeedData[j][0].append(jointFrameSpeed)

        axisLabels = ["$\Delta s$"]
        order = self.order + 1
        jointSpeedDataObj = JointDataClasses.JointDataDifferential(self.joints, axisLabels, jointSpeedData, self.dataType, order)
        return jointSpeedDataObj

class JointDataRotationalSpeed(JointDataSpeed):

    def __init__(self, joints, axisLabels, data):
        JointData.__init__(self, joints, axisLabels, data)
        self.axes = rotationalSpeedAxis()
        self.dataType = "Rotation Speed"
        self.order = 1
class JointDataDifferential(JointDataSpeed):

    def __init__(self, joints, axisLabels, data, dataType, order):
        JointData.__init__(self, joints, axisLabels, data)
        self.axes = differentialAxis()

        type = dataType[0:len(dataType) - 6]
        print(type)

        self.order = order
        suffix = "th"
        if self.order == 2:
            suffix = "nd"
        elif self.order == 3:
            suffix = "rd"

        self.dataType = str(self.order) + suffix + " Order " + type + " Differential"

class JointDataVectorSpeed(JointDataSpeed):

    def __init__(self, joints, axisLabels, data, dataType):
        JointData.__init__(self, joints, axisLabels, data)
        self.axes = vectorSpeedAxis()
        self.dataType = dataType
        self.order = 1

class JointDataVectorVelocity(JointDataVectors):

    def __init__(self, joints, axisLabels, data, dataType):
        JointData.__init__(self, joints, axisLabels, data)
        self.axes = vectorVelocityAxes()
        self.dataType = dataType

# class to define x, y, x axes
class vector3Axes():

    def __init__(self):

        self.x = "x"
        self.y = "y"
        self.z = "z"

# class to define x, y, x, w axes
class quaternionAxes():

    def __init__(self):

        self.x = "x"
        self.y = "y"
        self.z = "z"
        self.w = "w"

class matrixAxes():
    def __init__(self):

        self.m00 = "m00"
        self.m01 = "m01"
        self.m02 = "m02"

        self.m10 = "m10"
        self.m11 = "m11"
        self.m12 = "m12"

        self.m20 = "m20"
        self.m21 = "m21"
        self.m22 = "m22"

class rotationalSpeedAxis():

    def __init__(self):
        self.speed = "deg/frame"

class vectorSpeedAxis():

    def __init__(self):
        self.speed = "$\Delta \Vert V \Vert$"

class differentialAxis():
    def __init__(self):
        self.differential = "$\Delta s$"

class vectorVelocityAxes():
    def __init__(self):
        self.x = "$\Delta x$"
        self.y = "$\Delta y$"
        self.z = "$\Delta z$"
