from datetime import datetime
from printer import Printer
from queue import PriorityQueue as pQ


def isGoal(currentBlock):
    if currentBlock.drt == "STANDING" and currentBlock.currentMap.mapSeq[currentBlock.xB1][currentBlock.yB1] == 9:
        return True
    else:
        return False


def isVisited(visited, block):
    for item in visited:
        if item.xB1 == block.xB1 and item.yB1 == block.yB1 \
                and item.xB2 == block.xB2 and item.yB2 == block.yB2 \
                and item.drt == block.drt and item.currentMap == block.currentMap:
            return True
        if item.xB1 == block.xB2 and item.yB1 == block.yB2 \
                and item.xB2 == block.xB1 and item.yB2 == block.yB1 \
                and item.drt == block.drt and item.drt == "SPLIT" and item.currentMap == block.currentMap:
            return True
    return False


class Engine:
    def __init__(self, srcMap, func, startBlock):
        self.srcMap = srcMap
        self.func = func
        self.startBlock = startBlock
        self.printer = Printer(srcMap, func, None)

    def findFuncSeq(self, xCoord, yCoord):
        for seq in self.func.funcSeq:
            if (xCoord, yCoord) == (seq[0], seq[1]):
                return seq[2:]
        return None

    def doToggleButton(self, block, xCoord, yCoord):
        currentMapSeq = block.currentMap.mapSeq
        funcSeq = self.findFuncSeq(xCoord, yCoord)
        for i in range(funcSeq[0]):
            bXCoord = funcSeq[2 * i + 1]
            bYCoord = funcSeq[2 * i + 2]
            if currentMapSeq[bXCoord][bYCoord] == 0:
                currentMapSeq[bXCoord][bYCoord] = 1
            elif currentMapSeq[bXCoord][bYCoord] == 1:
                currentMapSeq[bXCoord][bYCoord] = 0

        otherSeq = funcSeq[1 + 2 * funcSeq[0]:]
        if len(otherSeq) > 0:
            for i in range(otherSeq[0]):
                value = otherSeq[3 * i + 1]
                bXCoord = otherSeq[3 * i + 2]
                bYCoord = otherSeq[3 * i + 3]
                currentMapSeq[bXCoord][bYCoord] = value

    def doOpenButton(self, block, xCoord, yCoord):
        currentMapSeq = block.currentMap.mapSeq
        funcSeq = self.findFuncSeq(xCoord, yCoord)
        for i in range(funcSeq[0]):
            bXCoord = funcSeq[2 * i + 1]
            bYCoord = funcSeq[2 * i + 2]
            if currentMapSeq[bXCoord][bYCoord] == 0:
                currentMapSeq[bXCoord][bYCoord] = 1

        otherSeq = funcSeq[1 + 2 * funcSeq[0]:]
        otherPair = len(otherSeq) // 2
        for i in range(otherPair):
            bXCoord = otherSeq[2 * i]
            bYCoord = otherSeq[2 * i + 1]
            currentMapSeq[bXCoord][bYCoord] = 0

    def doCloseButton(self, block, xCoord, yCoord):
        currentMapSeq = block.currentMap.mapSeq
        funcSeq = self.findFuncSeq(xCoord, yCoord)
        for i in range(funcSeq[0]):
            bXCoord = funcSeq[2 * i + 1]
            bYCoord = funcSeq[2 * i + 2]
            if currentMapSeq[bXCoord][bYCoord] == 1:
                currentMapSeq[bXCoord][bYCoord] = 0

        otherSeq = funcSeq[1 + 2 * funcSeq[0]:]
        otherPair = len(otherSeq) // 2
        for i in range(otherPair):
            bXCoord = otherSeq[2 * i]
            bYCoord = otherSeq[2 * i + 1]
            currentMapSeq[bXCoord][bYCoord] = 1

    def doSplit(self, block, xCoord, yCoord):
        funcSeq = self.findFuncSeq(xCoord, yCoord)
        block.splitBlock(funcSeq[1], funcSeq[2], funcSeq[3], funcSeq[4], funcSeq[0])

    def checkBlockAndDoFunc(self, block):
        currentMapSeq = block.currentMap.mapSeq
        if block.xB1 < 0 or block.xB1 >= block.currentMap.mapRow \
                or block.yB1 < 0 or block.yB1 >= block.currentMap.mapCol \
                or block.xB2 < 0 or block.xB2 >= block.currentMap.mapRow \
                or block.yB2 < 0 or block.yB2 >= block.currentMap.mapCol:
            return False

        if block.drt == "STANDING":
            if currentMapSeq[block.xB1][block.yB1] == 2:
                return False

            if currentMapSeq[block.xB1][block.yB1] == 6:
                self.doToggleButton(block, block.xB1, block.yB1)

            if currentMapSeq[block.xB1][block.yB1] == 7:
                self.doOpenButton(block, block.xB1, block.yB1)

            if currentMapSeq[block.xB1][block.yB1] == 8:
                self.doSplit(block, block.xB1, block.yB1)

        if block.selectedSplit != 2:

            if currentMapSeq[block.xB1][block.yB1] == 3:
                self.doToggleButton(block, block.xB1, block.yB1)

            if currentMapSeq[block.xB1][block.yB1] == 4:
                self.doOpenButton(block, block.xB1, block.yB1)

            if currentMapSeq[block.xB1][block.yB1] == 5:
                self.doCloseButton(block, block.xB1, block.yB1)

        if block.drt != "STANDING" and block.selectedSplit != 1:

            if currentMapSeq[block.xB2][block.yB2] == 3:
                self.doToggleButton(block, block.xB2, block.yB2)

            if currentMapSeq[block.xB2][block.yB2] == 4:
                self.doOpenButton(block, block.xB2, block.yB2)

            if currentMapSeq[block.xB2][block.yB2] == 5:
                self.doCloseButton(block, block.xB2, block.yB2)

        if currentMapSeq[block.xB1][block.yB1] == 0 or currentMapSeq[block.xB2][block.yB2] == 0:
            return False

        return True

    def move(self, stack, visited, block):
        if block is None:
            return
        if self.checkBlockAndDoFunc(block):
            if isVisited(visited, block):
                return
            stack.append(block)

    def calcRealStep(self, block):
        parentBlock = block
        while parentBlock:
            self.printer.stat.countStep += 1
            parentBlock = parentBlock.parentNode

    def DFS(self):
        stack = []
        visited = []
        stack.append(self.startBlock)
        self.printer.stat.virtualStep = + 1

        while stack:
            currentBlock = stack.pop()
            visited.append(currentBlock)
            # self.printer.printCurrentMap(currentBlock)

            if isGoal(currentBlock):
                self.printer.endBlock = currentBlock
                self.printer.stat.runningTime = datetime.now() - self.printer.stat.startTime
                self.calcRealStep(currentBlock)
                self.printer.stat.status = "SUCCESS"
                return

            else:
                if currentBlock.drt != "SPLIT":
                    self.printer.stat.virtualStep += 4
                    self.move(stack, visited, currentBlock.moveLeft())
                    self.move(stack, visited, currentBlock.moveRight())
                    self.move(stack, visited, currentBlock.moveUp())
                    self.move(stack, visited, currentBlock.moveDown())


                else:
                    self.printer.stat.virtualStep += 8
                    self.move(stack, visited, currentBlock.moveB1Left())
                    self.move(stack, visited, currentBlock.moveB1Right())
                    self.move(stack, visited, currentBlock.moveB1Up())
                    self.move(stack, visited, currentBlock.moveB1Down())

                    self.move(stack, visited, currentBlock.moveB2Left())
                    self.move(stack, visited, currentBlock.moveB2Right())
                    self.move(stack, visited, currentBlock.moveB2Up())
                    self.move(stack, visited, currentBlock.moveB2Down())

    def BFS(self):
        queue = []
        visited = []
        queue.append(self.startBlock)
        self.printer.stat.virtualStep = + 1

        while queue:
            currentBlock = queue.pop(0)
            visited.append(currentBlock)

            if isGoal(currentBlock):
                self.printer.endBlock = currentBlock
                self.printer.stat.runningTime = datetime.now() - self.printer.stat.startTime
                self.calcRealStep(currentBlock)
                self.printer.stat.status = "SUCCESS"
                return

            else:
                if currentBlock.drt != "SPLIT":
                    self.printer.stat.virtualStep += 4
                    self.move(queue, visited, currentBlock.moveLeft())
                    self.move(queue, visited, currentBlock.moveRight())
                    self.move(queue, visited, currentBlock.moveUp())
                    self.move(queue, visited, currentBlock.moveDown())


                else:
                    self.printer.stat.virtualStep += 8
                    self.move(queue, visited, currentBlock.moveB1Left())
                    self.move(queue, visited, currentBlock.moveB1Right())
                    self.move(queue, visited, currentBlock.moveB1Up())
                    self.move(queue, visited, currentBlock.moveB1Down())

                    self.move(queue, visited, currentBlock.moveB2Left())
                    self.move(queue, visited, currentBlock.moveB2Right())
                    self.move(queue, visited, currentBlock.moveB2Up())
                    self.move(queue, visited, currentBlock.moveB2Down())

    def distanceToEnd(self, block):
        xEndCoord = self.srcMap.endCoord[0]
        yEndCoord = self.srcMap.endCoord[1]
        B1ToEnd = (block.xB1 - xEndCoord) ** 2 + (block.yB1 - yEndCoord) ** 2
        B2ToENd = (block.xB2 - xEndCoord) ** 2 + (block.yB2 - yEndCoord) ** 2

        return int((B1ToEnd + B2ToENd) / 2)

    def moveBest(self, pQueue, visited, block):
        if block is None:
            return
        if self.checkBlockAndDoFunc(block):
            if isVisited(visited, block):
                return
            pQueue.put((block.costG + self.distanceToEnd(block), block))

    def PriorityDistanceFS(self):
        pQueue = pQ()
        visited = []
        pQueue.put((self.startBlock.costG + self.distanceToEnd(self.startBlock), self.startBlock))
        self.printer.stat.virtualStep = + 1

        while pQueue.not_empty:
            _, currentBlock = pQueue.get()
            visited.append(currentBlock)

            if isGoal(currentBlock):
                self.printer.endBlock = currentBlock
                self.printer.stat.runningTime = datetime.now() - self.printer.stat.startTime
                self.calcRealStep(currentBlock)
                self.printer.stat.status = "SUCCESS"
                return

            else:
                if currentBlock.drt != "SPLIT":
                    self.printer.stat.virtualStep += 4
                    self.moveBest(pQueue, visited, currentBlock.moveLeft())
                    self.moveBest(pQueue, visited, currentBlock.moveRight())
                    self.moveBest(pQueue, visited, currentBlock.moveUp())
                    self.moveBest(pQueue, visited, currentBlock.moveDown())


                else:
                    self.printer.stat.virtualStep += 8
                    self.moveBest(pQueue, visited, currentBlock.moveB1Left())
                    self.moveBest(pQueue, visited, currentBlock.moveB1Right())
                    self.moveBest(pQueue, visited, currentBlock.moveB1Up())
                    self.moveBest(pQueue, visited, currentBlock.moveB1Down())

                    self.moveBest(pQueue, visited, currentBlock.moveB2Left())
                    self.moveBest(pQueue, visited, currentBlock.moveB2Right())
                    self.moveBest(pQueue, visited, currentBlock.moveB2Up())
                    self.moveBest(pQueue, visited, currentBlock.moveB2Down())
