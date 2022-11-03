import sys
import time
from multiprocessing import Process, Manager

import pyautogui as pyautogui
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path
from selenium.webdriver.common.by import By

from block import Block
from engine import Engine
from func import Func
from map import Map
from stat_info import Stat


def readInput(input_file):
    # open file
    with open(input_file) as f:
        # read first line
        map_row, map_col, row_start, col_start, numFunc = [int(x) for x in next(f).split()]

        # read list function's sequence
        func_seq = []
        for _ in range(numFunc):
            func_seq.append([int(x) for x in next(f).split()])

        # read map
        map_seq = []
        for _ in range(map_row):
            map_seq.append([int(x) for x in next(f).split()])

    return map_row, map_col, row_start, col_start, map_seq, func_seq


def mainFunc(map_mode, is_visual, algorithm, processing, engine_list):
    if processing:
        engine_list = []
        is_visual = False

    if is_visual:
        service_object = Service(binary_path)
        driver = webdriver.Chrome(service=service_object)
        driver.get("https://www.mathplayground.com/logic_bloxorz.html")
        driver.maximize_window()
    try:
        if is_visual:
            time.sleep(3)
            shadow_host = driver.find_element(By.TAG_NAME, 'ruffle-player')
            driver.execute_script(
                "arguments[0].scrollIntoView({'block':'center','inline':'center'})",
                shadow_host)
            shadow_root = shadow_host.shadow_root
            myElem = shadow_root.find_element(By.ID, 'play_button')
            if myElem.get_attribute("style") == "display: block;":
                myElem.click()
                time.sleep(12)
                nextStepProcess = True
            else:
                nextStepProcess = True
        else:
            nextStepProcess = True

        if nextStepProcess:
            if map_mode != "all":
                if is_visual:
                    passCode = [i for i in open("passcode.txt").readlines()[int(map_mode) - 1][18:-1]]

                    pyautogui.click(607, 582)
                    time.sleep(1)
                    pyautogui.press(passCode, interval=0.1)
                    pyautogui.click(650, 621)
                    time.sleep(6)

                start = int(map_mode)
                end = start

            else:
                if is_visual:
                    pyautogui.click(607, 562)
                    time.sleep(2)
                    pyautogui.click(912, 688)
                    time.sleep(6)

                start = 1
                end = 10

            for i in range(start):
                engine_list.append(None)

            for i in range(start, end + 1):
                if processing:
                    inputFile = "input/map-{num:02d}.txt".format(num=i)

                    mapRow, mapCol, rowStart, colStart, mapSeq, funcSeq = readInput(inputFile)

                    # SET STAT

                    if algorithm == "DFS":
                        DFSStat = Stat("DFS Stat")
                    elif algorithm == "BFS":
                        BFSStat = Stat("BFS Stat")
                    elif algorithm == "ASTAR":
                        ASTARStat = Stat("ASTAR Stat")

                    # SET MAP
                    srcMap = Map(mapSeq, mapRow, mapCol)

                    # SET FUNCTION MAP
                    func = Func(funcSeq)

                    # SET BLOCK
                    block = Block(rowStart, colStart, rowStart, colStart, "STANDING", None, srcMap)

                    # SET ENGINE
                    engine = Engine(srcMap, func, block)

                    # RUN
                    if algorithm == "DFS":
                        engine.printer.stat = DFSStat
                        engine.DFS()
                    elif algorithm == "BFS":
                        engine.printer.stat = BFSStat
                        engine.BFS()
                    elif algorithm == "ASTAR":
                        engine.printer.stat = ASTARStat
                        engine.PriorityDistanceFS()

                    engine_list.append(engine)
                    continue

                if is_visual:
                    engine_list[i].printer.doRoad()

                    engine_list[i].printer.pressListKey()
                    if start == end:
                        time.sleep(3)
                    else:
                        time.sleep(6)

                else:
                    engine_list[i].printer.printRoad()
                    print(engine_list[i].printer.listKey)
        if processing:
            return engine_list
        else:
            return None

    except TimeoutException as ex:
        print(ex)
    finally:
        if is_visual:
            driver.quit()


def doDFS(map_mode, is_visual, algorithm, return_dict):
    engineListDFS = mainFunc(map_mode, is_visual, algorithm, 1, None)
    return_dict[0] = engineListDFS


def doBFS(map_mode, is_visual, algorithm):
    engineListBFS = mainFunc(map_mode, is_visual, algorithm, 1, None)
    # if engineListBFS:
    #     mainFunc(map_mode, is_visual, algorithm, 0, engineListBFS)


def doASTAR(map_mode, is_visual, algorithm):
    engineListASTAR = mainFunc(map_mode, is_visual, algorithm, 1, None)
    # if engineListASTAR:
    #     mainFunc(map_mode, is_visual, algorithm, 0, engineListASTAR)


if __name__ == '__main__':
    mapMode = sys.argv[1]
    isVisual = (int(sys.argv[2]) == 1)
    algorithm = sys.argv[3]

    manager = Manager()
    return_dict = manager.dict()
    return_dict[0] = None
    return_dict[1] = None
    return_dict[3] = None

    if algorithm == "DFS":
        dfsThread = Process(target=doDFS, args=(mapMode, isVisual, algorithm, return_dict))
        dfsThread.start()
        dfsThread.join(timeout=2)
        dfsThread.terminate()
        if return_dict[0]:
            mainFunc(mapMode, isVisual, algorithm, 0, return_dict[0])

    elif algorithm == "BFS":
        pass
    elif algorithm == "ASTAR":
        pass
    elif algorithm == "BEST" and not isVisual:
        pass

    sys.exit()
