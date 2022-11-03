from map import Map
from copy import deepcopy


class Block:

    # Coordinates 2 square block and direction
    def __init__(self, xB1, yB1, xB2, yB2, drt, parentNode, currentMap):
        self.xB1 = xB1
        self.yB1 = yB1
        self.xB2 = xB2
        self.yB2 = yB2
        self.drt = drt
        self.selectedSplit = 0
        self.parentNode = parentNode
        self.currentMap = currentMap
        self.keyPress = None

    # Compare self with other block
    def __lt__(self, block):
        return True

    def __gt__(self, block):
        return True

    def printBlock(self):
        print(self.xB1, self.yB1, self.xB2, self.yB2, self.drt, self.selectedSplit)

    def newCopyMap(self):
        return Map(deepcopy(self.currentMap.mapSeq), self.currentMap.mapRow, self.currentMap.mapCol)

    def splitBlock(self, xB1, yB1, xB2, yB2, selectedSplit):
        self.xB1 = xB1
        self.yB1 = yB1
        self.xB2 = xB2
        self.yB2 = yB2
        self.drt = "SPLIT"
        self.selectedSplit = selectedSplit
        self.keyPress = self.keyPress + ", WAIT"

    def moveUp(self):
        nextBlock = Block(self.xB1, self.yB1, self.xB2, self.yB2, "STANDING", self, self.newCopyMap())
        nextBlock.selectedSplit = 0
        nextBlock.keyPress = "UP"
        if self.drt == "STANDING":
            nextBlock.xB1 -= 2
            nextBlock.xB2 -= 1
            nextBlock.drt = "LYING_COL"
        elif self.drt == "LYING_ROW":
            nextBlock.xB1 -= 1
            nextBlock.xB2 -= 1
            nextBlock.drt = "LYING_ROW"
        elif self.drt == "LYING_COL":
            nextBlock.xB1 -= 1
            nextBlock.xB2 -= 2
            nextBlock.drt = "STANDING"
        else:
            return None
        return nextBlock

    def moveDown(self):
        nextBlock = Block(self.xB1, self.yB1, self.xB2, self.yB2, "STANDING", self, self.newCopyMap())
        nextBlock.selectedSplit = 0
        nextBlock.keyPress = "DOWN"
        if self.drt == "STANDING":
            nextBlock.xB1 += 1
            nextBlock.xB2 += 2
            nextBlock.drt = "LYING_COL"
        elif self.drt == "LYING_ROW":
            nextBlock.xB1 += 1
            nextBlock.xB2 += 1
            nextBlock.drt = "LYING_ROW"
        elif self.drt == "LYING_COL":
            nextBlock.xB1 += 2
            nextBlock.xB2 += 1
            nextBlock.drt = "STANDING"
        else:
            return None
        return nextBlock

    def moveLeft(self):
        nextBlock = Block(self.xB1, self.yB1, self.xB2, self.yB2, "STANDING", self, self.newCopyMap())
        nextBlock.selectedSplit = 0
        nextBlock.keyPress = "LEFT"
        if self.drt == "STANDING":
            nextBlock.yB1 -= 2
            nextBlock.yB2 -= 1
            nextBlock.drt = "LYING_ROW"
        elif self.drt == "LYING_ROW":
            nextBlock.yB1 -= 1
            nextBlock.yB2 -= 2
            nextBlock.drt = "STANDING"
        elif self.drt == "LYING_COL":
            nextBlock.yB1 -= 1
            nextBlock.yB2 -= 1
            nextBlock.drt = "LYING_COL"
        else:
            return None
        return nextBlock

    def moveRight(self):
        nextBlock = Block(self.xB1, self.yB1, self.xB2, self.yB2, "STANDING", self, self.newCopyMap())
        nextBlock.selectedSplit = 0
        nextBlock.keyPress = "RIGHT"
        if self.drt == "STANDING":
            nextBlock.yB1 += 1
            nextBlock.yB2 += 2
            nextBlock.drt = "LYING_ROW"
        elif self.drt == "LYING_ROW":
            nextBlock.yB1 += 2
            nextBlock.yB2 += 1
            nextBlock.drt = "STANDING"
        elif self.drt == "LYING_COL":
            nextBlock.yB1 += 1
            nextBlock.yB2 += 1
            nextBlock.drt = "LYING_COL"
        else:
            return None
        return nextBlock

    def moveB1Up(self):
        if self.drt == "SPLIT":
            nextBlock = Block(self.xB1 - 1, self.yB1, self.xB2, self.yB2, "SPLIT", self, self.newCopyMap())
            nextBlock.selectedSplit = 1
            if self.selectedSplit == 2:
                nextBlock.keyPress = "SPACE, UP"
            else:
                nextBlock.keyPress = "UP"
            nextBlock.checkMerge()
            return nextBlock
        else:
            return None

    def moveB1Down(self):
        if self.drt == "SPLIT":
            nextBlock = Block(self.xB1 + 1, self.yB1, self.xB2, self.yB2, "SPLIT", self, self.newCopyMap())
            nextBlock.selectedSplit = 1
            if self.selectedSplit == 2:
                nextBlock.keyPress = "SPACE, DOWN"
            else:
                nextBlock.keyPress = "DOWN"
            nextBlock.checkMerge()
            return nextBlock
        else:
            return None

    def moveB1Left(self):
        if self.drt == "SPLIT":
            nextBlock = Block(self.xB1, self.yB1 - 1, self.xB2, self.yB2, "SPLIT", self, self.newCopyMap())
            nextBlock.selectedSplit = 1
            if self.selectedSplit == 2:
                nextBlock.keyPress = "SPACE, LEFT"
            else:
                nextBlock.keyPress = "LEFT"
            nextBlock.checkMerge()
            return nextBlock
        else:
            return None

    def moveB1Right(self):
        if self.drt == "SPLIT":
            nextBlock = Block(self.xB1, self.yB1 + 1, self.xB2, self.yB2, "SPLIT", self, self.newCopyMap())
            nextBlock.selectedSplit = 1
            if self.selectedSplit == 2:
                nextBlock.keyPress = "SPACE, RIGHT"
            else:
                nextBlock.keyPress = "RIGHT"
            nextBlock.checkMerge()
            return nextBlock
        else:
            return None

    def moveB2Up(self):
        if self.drt == "SPLIT":
            nextBlock = Block(self.xB1, self.yB1, self.xB2 - 1, self.yB2, "SPLIT", self, self.newCopyMap())
            nextBlock.selectedSplit = 2
            if self.selectedSplit == 1:
                nextBlock.keyPress = "SPACE, UP"
            else:
                nextBlock.keyPress = "UP"
            nextBlock.checkMerge()
            return nextBlock
        else:
            return None

    def moveB2Down(self):
        if self.drt == "SPLIT":
            nextBlock = Block(self.xB1, self.yB1, self.xB2 + 1, self.yB2, "SPLIT", self, self.newCopyMap())
            nextBlock.selectedSplit = 2
            if self.selectedSplit == 1:
                nextBlock.keyPress = "SPACE, DOWN"
            else:
                nextBlock.keyPress = "DOWN"
            nextBlock.checkMerge()
            return nextBlock
        else:
            return None

    def moveB2Left(self):
        if self.drt == "SPLIT":
            nextBlock = Block(self.xB1, self.yB1, self.xB2, self.yB2 - 1, "SPLIT", self, self.newCopyMap())
            nextBlock.selectedSplit = 2
            if self.selectedSplit == 1:
                nextBlock.keyPress = "SPACE, LEFT"
            else:
                nextBlock.keyPress = "LEFT"
            nextBlock.checkMerge()
            return nextBlock
        else:
            return None

    def moveB2Right(self):
        if self.drt == "SPLIT":
            nextBlock = Block(self.xB1, self.yB1, self.xB2, self.yB2 + 1, "SPLIT", self, self.newCopyMap())
            nextBlock.selectedSplit = 2
            if self.selectedSplit == 1:
                nextBlock.keyPress = "SPACE, RIGHT"
            else:
                nextBlock.keyPress = "RIGHT"
            nextBlock.checkMerge()
            return nextBlock
        else:
            return None

    def checkMerge(self):
        if self.xB1 == self.xB2:
            if self.yB1 - self.yB2 == 1:
                self.yB1 -= 1
                self.yB2 += 1
                self.drt = "LYING_ROW"
            elif self.yB1 - self.yB2 == -1:
                self.drt = "LYING_ROW"
            else:
                self.drt = "SPLIT"
        elif self.yB1 == self.yB2:
            if self.xB1 - self.xB2 == 1:
                self.xB1 -= 1
                self.xB2 += 1
                self.drt = "LYING_COL"
            elif self.xB1 - self.xB2 == -1:
                self.drt = "LYING_COL"
            else:
                self.drt = "SPLIT"
        else:
            self.drt = "SPLIT"
