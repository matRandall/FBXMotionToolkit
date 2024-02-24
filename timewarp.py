import numpy as np
import matplotlib.pyplot as plt

def accumulatedCostMatrix(costMatrix):

    totalCostMatrix = np.empty(costMatrix.shape)

    for targetFrame in range(totalCostMatrix.shape[1]):
        for inputFrame in range(totalCostMatrix.shape[0]):
            if(targetFrame == 0 and inputFrame == 0):
                totalCostMatrix[0, 0] = costMatrix[0, 0]
            else:
                stepChoices = []
                if inputFrame - 1 >= 0:
                    stepChoices.append(
                        costMatrix[inputFrame, targetFrame] + totalCostMatrix[inputFrame - 1, targetFrame])
                if targetFrame - 1 >= 0:
                    stepChoices.append(
                        costMatrix[inputFrame, targetFrame] + totalCostMatrix[inputFrame, targetFrame - 1])
                if inputFrame - 1 >= 0 and targetFrame - 1 >= 0:
                    stepChoices.append(
                        costMatrix[inputFrame, targetFrame] + totalCostMatrix[inputFrame - 1, targetFrame - 1])

                stepChoices.sort()

                totalCostMatrix[inputFrame, targetFrame] = stepChoices[0]

    return totalCostMatrix

def plotDTW(totalCostMatrix):

    # set initial search position to top right of cost matrix
    lPos = (totalCostMatrix.shape[0] - 1, totalCostMatrix.shape[1] - 1)

    # start list with last position on DTW map
    DTWmap = [lPos[0]]

    # loop until we reach the start of the input signal
    while lPos[0] > 0 or lPos[1] > 0:

        # at the o frame on reference then just delete
        if lPos[0] == 0:
            lNextMove = "insert"

        # at the 0 frame on input motion then insert
        elif lPos[1] == 0:
            lNextMove = "delete"

        # else check which move will have the lowest cost
        else:
            lNextMove = "match"
            lLowestVal = totalCostMatrix[lPos[0] - 1, lPos[1] - 1]
            if totalCostMatrix[lPos[0] - 1, lPos[1]] < lLowestVal:
                lNextMove = "delete"
                lLowestVal = totalCostMatrix[lPos[0] - 1, lPos[1]]
            if totalCostMatrix[lPos[0], lPos[1] - 1] < lLowestVal:
                lNextMove = "insert"

        # update position and DTW map based opn the next move
        if lNextMove == "match":
            lPos = (lPos[0] - 1, lPos[1] - 1)
            DTWmap.insert(0, lPos[0])
        elif lNextMove == "delete":
            lPos = (lPos[0] - 1, lPos[1])
            # update most recent map value if not already reached the start if the reference motion
            if lPos[1] > 0:
                DTWmap[0] = lPos[0]
        elif lNextMove == "insert":
            lPos = (lPos[0], lPos[1] - 1)
            DTWmap.insert(0, lPos[0])

    return np.array(DTWmap)

def graphDTW(costMatrix, **kwargs):

    DTWmap = kwargs.get('DTWmap', np.array([]))

    np_totalCostMatrix = np.array(costMatrix)
    np_totalCostMatrix = np.transpose(costMatrix)

    ax = plt.gca()
    ax.set_aspect("equal")
    plt.pcolormesh(np_totalCostMatrix, rasterized=True)

    if DTWmap.shape[0] > 0:
        y = np.arange(0, np_totalCostMatrix.shape[0])
        plt.plot(DTWmap, y, color='r')

    ax.set_xlabel("Input motion (frames)")
    ax.set_ylabel("Target motion (frames)")

    plt.show()