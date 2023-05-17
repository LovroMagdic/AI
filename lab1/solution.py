import codecs
import argparse
import heapq

def path(start, goal, states):
    sum = 0
    result = list()
    result.append(goal)
    while (states[goal])[0] != "NULL":
        result.append((states[goal])[0])
        sum = sum + int((states[goal])[1])
        goal = (states[goal])[0]
    path = result[::-1]
    return path, sum        

def BFS(start, goal, graph):
    sum = 0
    q = []
    closed = dict()
    states = dict()
    
    q.append(start)
    states[start] = ["NULL"] + [0]

    while q:
        visited = q.pop(0)
        for each in graph[visited]:
            if each.split(",")[0] not in closed:
                q.append(each.split(",")[0])
                if each.split(",")[0] not in states.keys():
                    states[each.split(",")[0]] = [visited] + [each.split(",")[1]]
        
        # closed.append(visited)
        closed[visited] = ["visited"]

        for each in goal:
            if each in closed:
                result, sum = path(start, each, states)
                print("# BFS")
                print("[FOUND_SOLUTION]: yes")
                print("[STATES_VISITED]: " + str(len(closed)))
                print("[PATH_LENGTH]: " + str(len(result)))
                print("[TOTAL_COST]: {:.1f}".format(sum))
                print("[PATH]: ", end="")
                print(' => '.join(result))
                return
    print("# BFS")
    print("[FOUND_SOLUTION]: no")
    return

def UCS(start, goal, graph):
    q = []
    closed = dict()
    states = dict()

    heapq.heapify(q)

    heapq.heappush(q, (0, start))
    states[start] = ["NULL"] + [0]
    

    while q:
        visited = heapq.heappop(q)
        closed[visited[1]] = ["visited"]

        for each in graph[visited[1]]:
            if each.split(",")[0] not in closed:
                heapq.heappush(q, (int(each.split(",")[1]) + int(visited[0]), str(each.split(",")[0])))

                if each.split(",")[0] not in states.keys():
                    states[each.split(",")[0]] = [visited[1]] + [int(each.split(",")[1])] + [int(each.split(",")[1]) + int(visited[0])]
                if each.split(",")[0] in states.keys() and int(each.split(",")[1]) + int(visited[0]) < (states[each.split(",")[0]])[2]:
                    states.pop(each.split(",")[0])
                    states[each.split(",")[0]] = [visited[1]] + [int(each.split(",")[1])] + [int(each.split(",")[1]) + int(visited[0])]

        for each in goal:
            if each in closed:
                if args.check_optimistic:
                    return visited[0]
                else:
                    result, sum = path(start, each, states)
                    print("# UCS")
                    print("[FOUND_SOLUTION]: yes")
                    print("[STATES_VISITED]: " + str(len(closed)))
                    print("[PATH_LENGTH]: " + str(len(result)))
                    print("[TOTAL_COST]: {:.1f}".format(sum))
                    print("[PATH]: ", end="")
                    print(' => '.join(result))
                    return sum
            
    print("# UCS")
    print("[FOUND_SOLUTION]: no")
    return

def A_STAR(start, goal, graph, h):
    q = []
    closed = dict()
    states = dict()

    heapq.heapify(q)

    heapq.heappush(q, (0, start))
    states[start] = ["NULL"] + [0] + [0]
    
    while q:
        visited = heapq.heappop(q)
        closed[visited[1]] = ["visited"]

        for each in graph[visited[1]]:
            if each.split(",")[0] not in closed:
                hv = int(h[each.split(",")[0]])
                heapq.heappush(q, ((int(each.split(",")[1]) + int(visited[0]) + hv), str(each.split(",")[0])))

                if each.split(",")[0] not in states.keys():
                    states[each.split(",")[0]] = [visited[1]] + [int(each.split(",")[1])] + [int(each.split(",")[1]) + int(visited[0]) + hv]
                if each.split(",")[0] in states.keys() and int(each.split(",")[1]) + int(visited[0]) + hv < (states[each.split(",")[0]])[2]:
                    states.pop(each.split(",")[0])
                    states[each.split(",")[0]] = [visited[1]] + [int(each.split(",")[1])] + [int(each.split(",")[1]) + int(visited[0]) + hv]

        for each in goal:
            if each in closed:
                result, sum = path(start, each, states)
                print("# A_STAR " + args.h)
                print("[FOUND_SOLUTION]: yes")
                print("[STATES_VISITED]: " + str(len(closed)))
                print("[PATH_LENGTH]: " + str(len(result)))
                print("[TOTAL_COST]: {:.1f}".format(float(sum)))
                print("[PATH]: ", end="")
                print(' => '.join(result))
                return

    print("# A_STAR " + args.h)
    print("[FOUND_SOLUTION]: no")
    return

def check_optimistic(graph, goal, h):
    print("# HEURISTIC-OPTIMISTIC " + args.h)
    flag_opt = True
    for node in graph:
        real_dist = UCS(node, goal, graph)
        if float(real_dist) >= float(h[node]):
            print("[CONDITION]: [OK] h(" + node + ") <= h*: {:.1f} <= {:.1f}".format(float(h[node]), float(real_dist)))
        else:
            flag_opt = False
            print("[CONDITION]: [ERR] h(" + node + ") <= h*: {:.1f} <= {:.1f}".format(float(h[node]), float(real_dist)))
    if flag_opt:
        print("[CONCLUSION]: Heuristic is optimistic.")
    else:
        print("[CONCLUSION]: Heuristic is not optimistic.")
    return

def check_consistent(graph, h):
    print("# HEURISTIC-CONSISTENT " + args.h)
    flag_cons = True
    for node in graph:
        for each in graph[node]:
            if float(h[node]) <= float(h[each.split(",")[0]]) + float(each.split(",")[1]):
                print("[CONDITION]: [OK] h(" + node + ") <= h(" + each.split(",")[0] + ") + c: {:.1f} <= {:.1f} + {:.1f}".format(float(h[node]), float(h[each.split(",")[0]]), float(each.split(",")[1])))
            else:
                flag_cons = False
                print("[CONDITION]: [ERR] h(" + node + ") <= h(" + each.split(",")[0] + ") + c: {:.1f} <= {:.1f} + {:.1f}".format(float(h[node]), float(h[each.split(",")[0]]), float(each.split(",")[1])))
    if flag_cons:
        print("[CONCLUSION]: Heuristic is consistent.")
    else:
        print("[CONCLUSION]: Heuristic is not consistent.")
    return

parser = argparse.ArgumentParser()
parser.add_argument('--alg', type=str)
parser.add_argument('--ss', type=str)
parser.add_argument('--h', type=str)
parser.add_argument('--check-optimistic', '--check_optimistic', action='store_true')
parser.add_argument('--check-consistent', '--check_consistent', action='store_true')
args = parser.parse_args()


f = codecs.open(args.ss, "r", "utf-8").readlines()
# f = open("istra.txt", "r").readlines()
f = [x.strip() for x in f]
for i in f:
    if i.startswith("#"):
        f.remove(i)

start = f.pop(0)
goal = f.pop(0).split()


f = [x.split(":") for x in f]
f = dict(f)
f = {key: list(map(str, value.split())) for key, value in f.items()}
graph = {i: sorted(j) for i, j in f.items()}


if args.h:
    h = codecs.open(args.h, "r", "utf-8").readlines()
    h = [x.strip() for x in h]
    h = [x.split(": ") for x in h]
    h = dict(h)
'''
h = {'Baderna': '25', 
'Barban': '35', 
'Buje': '21', 
'Grožnjan': '17', 
'Kanfanar': '30', 
'Labin': '35', 
'Lupoglav': '35', 
'Medulin': '61', 
'Motovun': '12', 
'Opatija': '26', 
'Pazin': '40', 
'Poreč': '32', 
'Pula': '57', 
'Rovinj': '40', 
'Umag': '31', 
'Višnjan': '20', 
'Vodnjan': '47', 
'Žminj': '27', 
'Buzet': '0'}

A_STAR(start, goal, graph, h)
'''
if not args.check_optimistic and not args.check_consistent:
    if args.alg == "bfs":
        BFS(start, goal, graph)
    elif args.alg == "ucs":
        UCS(start, goal, graph)
    elif args.alg == "astar":
        A_STAR(start, goal, graph, h)
elif args.check_optimistic:
    check_optimistic(graph, goal, h)
elif args.check_consistent:
    check_consistent(graph, h)