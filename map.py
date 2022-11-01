class Map:
    def __init__(self, mapSeq, mapRow, mapCol):
        self.mapSeq = mapSeq
        self.mapRow = mapRow
        self.mapCol = mapCol

    def isEqual(self, otherMap):
        return otherMap.mapSeq == self.mapSeq
