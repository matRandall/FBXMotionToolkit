from FBXSequence import FBXSequence

def importFBXSequence(filepath):
    importedSeq = FBXSequence(filepath)
    return importedSeq

class animationCurveType():
    TRANSLATION = "translation"
    ROTATION = "rotation"

class axis():
    X = 0
    Y = 1
    Z = 2

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


