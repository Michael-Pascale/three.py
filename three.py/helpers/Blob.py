## contains a gridgroup, with some additional functionality for editing the group
class Blop(object):

    def __init__(self, group):
        super().__init__()
        self.group = group


    def moveSector(self, sector_old, sector_new):
        pass

    def movePointWithinSector(self, sector, point_old, point_new):
        pass

    def movePointToNewSector(self, sector_old, point_old, sector_new, point_new):
        pass

    def removePoint(self, sector, point):
        pass

    def removeSector(self, sector):
        pass

    def addSector(self, sector):
        pass

    def addPointsToSector(self, sector):
        pass

    def modifySector(self, sector, points):
        pass
