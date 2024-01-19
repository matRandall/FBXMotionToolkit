import numpy as np
import sys
import scipy.stats as stats

def measureDistanceSimilarity(inputMotionJointData, targetMotionJointData):
    motion1 = inputMotionJointData
    motion2 = targetMotionJointData

    # check data integrity
    motion1.errorCheckMatchingFrameCount(motion2)
    motion1.errorCheckMatchingJointCount(motion2)
    motion1.errorCheckMatchingClass(motion2)
    motion1.errorCheckHasDifferenceFunction()

    sum = 0

    for f in range(motion1.getFrameCount()):
        d = motion1.getDifferenceBetweenFrames(motion1.joints, f, motion2, f)
        sum += d

    avgDist = sum / (motion1.getJointCount() * motion2.getFrameCount())

    return avgDist

def measureCorrelationSimilarity(inputFlatJointData, targetFlatJointData, method, **kwargs):

    # check data integrity
    if inputFlatJointData.shape[0] != targetFlatJointData.shape[0]:
        print("The two sets of data do not have a matching numbers of joint axis")
        sys.exit()

    if inputFlatJointData.shape[1] != targetFlatJointData.shape[1]:
        print("The two sets of data do not have a matching numbers of frames")
        sys.exit()

    minThreshold = kwargs.get("minThreshold", 0.001)
    testTotal = 0

    for i in range(inputFlatJointData.shape[0]):
        inputAxis = inputFlatJointData[i]
        targetAxis = targetFlatJointData[i]
        inputRange = np.max(inputAxis) - np.min(inputAxis)
        targetRange = np.max(targetAxis) - np.min(targetAxis)

        if inputRange > minThreshold or targetRange > minThreshold:

            if method == CorrelationMethod.Pearson:
                score, pVal = stats.pearsonr(inputAxis, targetAxis)
            elif method == CorrelationMethod.Spearmans:
                score, pVal = stats.spearmanr(inputAxis, targetAxis)
            elif method == CorrelationMethod.KendallTau:
                score, pVal = stats.kendalltau(inputAxis, targetAxis, method="asymptotic")

            #print(score)
            testTotal += score

        else:

            testTotal += 1.

    avgTotal = testTotal / inputFlatJointData.shape[0]
    return avgTotal

def getSimilarityMatrix(inputMotionJointData, targetMotionJointData):
    motion1 = inputMotionJointData
    motion2 = targetMotionJointData

    # check data integrity
    motion1.errorCheckMatchingJointCount(motion2)
    motion1.errorCheckMatchingClass(motion2)
    motion1.errorCheckHasDifferenceFunction()

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

class CorrelationMethod():
    Pearson = "Pearson"
    Spearmans = "Spearman"
    KendallTau = "KendallTau"