import time

import pyautogui


class Printer:
    def __init__(self, srcMap, func, stat):
        self.map = srcMap
        self.endBlock = None
        self.func = func
        self.stat = stat
        self.listKey = []

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
                listKeyPress = block.keyPress.split(", ")
                self.listKey += listKeyPress
                print(block.keyPress, end=" -- ")
                block.printBlock()
            else:
                print("START", end=" -- ")
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
            self.printInitMap()
            print("===============================")

    def printStat(self):
        print()
        print("============ STAT =============")
        print("STATUS: " + str(self.stat.status))
        print("RUNNING TIME: " + str(self.stat.runningTime))
        print("REAL STEP: " + str(self.stat.countStep))
        print("VIRTUAL STEP: " + str(self.stat.virtualStep))
        print("===============================")

    def pressListKey(self):
        for i in self.listKey:
            if i == "UP":
                pyautogui.keyDown("up")
                pyautogui.keyUp("up")
            elif i == "DOWN":
                pyautogui.keyDown("down")
                pyautogui.keyUp("down")
            elif i == "LEFT":
                pyautogui.keyDown("left")
                pyautogui.keyUp("left")
            elif i == "RIGHT":
                pyautogui.keyDown("right")
                pyautogui.keyUp("right")
            elif i == "SPACE":
                pyautogui.keyDown("space")
                pyautogui.keyUp("space")
            else:
                time.sleep(0.6)
            time.sleep(0.05)

    def doRoad(self):
        self.listKey = []
        self.stat.countStep = 0
        self.doRoadRev(self.endBlock)
        self.printStat()

    def doRoadRev(self, currentBlock):
        if currentBlock is None:
            self.stat.status = "SUCCESS"
        else:
            self.stat.countStep += 1
            self.doRoadRev(currentBlock.parentNode)
            self.doCurrentMap(currentBlock)

    def doCurrentMap(self, block):
        if block:
            if block.keyPress:
                listKeyPress = block.keyPress.split(", ")
                self.listKey += listKeyPress
                print(block.keyPress, end=" -- ")
                block.printBlock()
            else:
                print("START", end=" -- ")
                block.printBlock()
        else:
            print()
            print("========= ERROR MAP ===========\n")
            self.printInitMap()
            print("===============================")

    def printRoad(self):
        self.listKey = []
        self.stat.countStep = 0
        self.printRoadRev(self.endBlock)
        self.printStat()

    def printRoadRev(self, currentBlock):
        if currentBlock is None:
            self.stat.status = "SUCCESS"
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
