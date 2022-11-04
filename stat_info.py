import os
from datetime import datetime

import psutil


class Stat:
    def __init__(self, name):
        self.name = name
        self.status = "FAIL"
        self.countStep = 0
        self.virtualStep = 0
        self.startTime = datetime.now()
        self.runningTime = 0
        self.process = psutil.Process(os.getpid())
        self.startMemory = self.process.memory_info().rss
        self.processMemory = 0

    def printStat(self, index):
        print()
        print("===== " + self.name + " {num:02d}".format(num=index) + " ======")
        print("STATUS: " + str(self.status))
        print("RUNNING TIME: " + str(self.runningTime))
        print("REAL STEP: " + str(self.countStep))
        print("VIRTUAL STEP: " + str(self.virtualStep))
        print("===============================")
