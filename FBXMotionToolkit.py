from FBXSequence import FBXSequence
import csv

def importFBXSequence(filepath):
    importedSeq = FBXSequence(filepath)
    return importedSeq

class animationCurveType():
    TRANSLATION = "translation"
    ROTATION = "rotation"

class axis():
    x = 0
    y = 1
    z = 2

class joint():
    root = "root"
    rhip = "rhip"
    rknee = "rknee"
    rankle = "rankle"
    rtoes = "rtoes"
    lhip = "lhip"
    lknee = "lknee"
    lankle = "lankle"
    ltoes = "ltoes"
    rshoulder = "rshoulder"
    relbow = "relbow"
    rwrist = "rwrist"
    lshoulder = "lshoulder"
    lelbow = "lelbow"
    lwrist = "lwrist"
    head = "head"
    neck = "neck"
    chest = "chest"
    belly = "belly"

def getJointTitle(theJoint):

    jointTitles = { joint.root : "Root",
                    joint.rhip : "Right Hip",
                    joint.rknee : "Right Knee",
                    joint.rankle : "Right Ankle",
                    joint.rtoes : "Right Toes",
                    joint.lhip : "Left Hip",
                    joint.lknee : "Left Knee",
                    joint.lankle : "Left Ankle",
                    joint.ltoes : "Left Toes",
                    joint.rshoulder : "Right Shoulder",
                    joint.relbow : "Right Elbow",
                    joint.rwrist : "Right Wrist",
                    joint.lshoulder : "Left Shoulder",
                    joint.lelbow : "Left Elbow",
                    joint.lwrist : "Left Wrist",
                    joint.head : "Head",
                    joint.neck : "Neck",
                    joint.chest : "Chest",
                    joint.belly : "Belly",
                    }

    return jointTitles[theJoint]

# reusable function for writing CSV ,data
def writeDataToCSV(file, data, header):
    with open(file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(header)
        for row in data:
            writer.writerow(row)

    csvfile.close()



