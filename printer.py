from stat_info import Stat


class Printer:
    def __init__(self, srcMap, func, stat):
        self.map = srcMap
        self.endBlock = None
        self.func = func
        self.stat = stat

    def printInitMap(self):
        print()
        stringBuilder = ""
        print("========== INIT MAP ===========\n")
        for row in range(self.map.mapRow):
            for col in range(self.map.mapCol):
                if self.map.mapSeq[row][col] == 0:
                    stringBuilder += "  "
                else:
                    stringBuilder += str(self.map.mapSeq[row][col]) + " "
            stringBuilder += "\n"
        print(stringBuilder)
        print("===============================")

    def printCurrentMap(self, block):
        stringBuilder = ""
        if block:
            currentMap = block.currentMap
            if block.keyPress:
                print(block.keyPress, end=" -- ")
                block.printBlock()
            else:
                block.printBlock()
            print("========= CURRENT MAP =========\n")
            for row in range(currentMap.mapRow):
                for col in range(currentMap.mapCol):
                    if (row == block.xB1 and col == block.yB1) or (
                            row == block.xB2 and col == block.yB2):
                        stringBuilder += "* "
                    elif currentMap.mapSeq[row][col] == 0:
                        stringBuilder += "  "
                    else:
                        stringBuilder += str(currentMap.mapSeq[row][col]) + " "
                stringBuilder += "\n"
            print(stringBuilder)
            print("===============================")
        else:
            print()
            print("========= ERROR MAP ===========\n")
            self.printStat()
            print("===============================")

    def printRoad(self):
        self.printRoadRev(self.endBlock)

    def printStat(self):
        print()
        print("============ STAT =============")
        print("REAL STEP: " + str(self.stat.countStep))
        print("VIRTUAL STEP: " + str(self.stat.virtualStep))
        print("===============================")

    def printRoadRev(self, currentBlock):
        if currentBlock is None:
            self.printStat()
        else:
            self.stat.countStep += 1
            self.printRoadRev(currentBlock.parentNode)
            self.printCurrentMap(currentBlock)

    def printListFunc(self):
        stringBuilder = ""
        for func in self.func.funcSeq:
            for i in func:
                stringBuilder += str(i) + " "
            stringBuilder += "\n"
        if stringBuilder == "":
            stringBuilder = "EMPTY LIST\n"
        print()
        print("======== LIST FUNCTION ========\n")
        print(stringBuilder)
        print("===============================")
