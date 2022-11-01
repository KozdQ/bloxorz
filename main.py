from block import Block
from engine import Engine
from func import Func
from map import Map


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


if __name__ == '__main__':
    inputFile = "input/map-02.txt"
    mapRow, mapCol, rowStart, colStart, mapSeq, funcSeq = readInput(inputFile)

    # SET MAP
    srcMap = Map(mapSeq, mapRow, mapCol)

    # SET FUNCTION MAP
    func = Func(funcSeq)

    # SET BLOCK
    block = Block(rowStart, colStart, rowStart, colStart, "STANDING", None, srcMap)

    engine = Engine(srcMap, func, block)

    engine.DFS()
