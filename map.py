class Map:
    def __init__(self, mapSeq, mapRow, mapCol):
        self.mapSeq = mapSeq
        self.mapRow = mapRow
        self.mapCol = mapCol
        self.endCoord = None
        for row in range(mapRow):
            for col in range(mapCol):
                if mapSeq[row][col] == 9:
                    self.endCoord = [row, col]

    def __eq__(self, otherMap):
        return otherMap.mapSeq == self.mapSeq
