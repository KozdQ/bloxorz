from subprocess import run

algorithm = "DFS"
for i in range(1, 34):
    data = run("python3 main.py {num:02d} 0 {alg} 0 0 > output-dfs/map-{num:02d}.txt".format(num=i, alg=algorithm), capture_output=True, shell=True)

algorithm = "BFS"
for i in range(1, 34):
    data = run("python3 main.py {num:02d} 0 {alg} 0 0 > output-bfs/map-{num:02d}.txt".format(num=i, alg=algorithm), capture_output=True, shell=True)

algorithm = "ASTAR"
for i in range(1, 34):
    data = run("python3 main.py {num:02d} 0 {alg} 0 0 > output-astar/map-{num:02d}.txt".format(num=i, alg=algorithm), capture_output=True, shell=True)

run("python3 main.py all 0 DFS 1 0")
run("python3 main.py all 0 BFS 1 0")
run("python3 main.py all 0 ASTAR 1 0")
