import sys

#want_list: courses wanted by each student
#cap_list: capacity of each course
#n: number of courses each student is required to take
def scheduleCheck(want_list, cap_list, n):
    if len(want_list) == 0: 
        return "Yes"

    size = len(studentList(want_list)) * n
    graph = buildFlowGraph(want_list, cap_list, n)
    flow = EdmondsKarp(graph)
    if flow != size:
        return "No"
    else:
        return "Yes"


def EdmondsKarp(graph):

    s=0
    t=(len(graph))-1

    parent = [-1]*(len(graph))
    maxFlow = 0

    while BreadthFirstSearch(graph, s, t, parent):
        pathFlow = float("Inf")
        j = t
        while(j != s):
            pathFlow = min(pathFlow, graph[parent[j]][j])
            j = parent[j]
        
        maxFlow += pathFlow

        v = t
        while(v != s):
            u = parent[v]
            graph[u][v] -= pathFlow
            graph[v][u] += pathFlow
            v = parent[v]
    
    return maxFlow

def BreadthFirstSearch(graph, s, t, parent):

    visited = [False]*(len(graph))
    queue = []

    queue.append(s)
    visited[s] = True

    while queue:
        u = queue.pop(0)

        for i, v in enumerate(graph[u]):
            if visited[i] == False and v > 0:
                queue.append(i)
                visited[i] = True
                parent[i] = u
                if i == t:
                    return True

    return False

def buildFlowGraph(want_list, cap_list, n):
    graph = []
    student_nodes = studentList(want_list)
    class_nodes = classList(cap_list)

    ref_dict = {"s": 0} #array that correlates the indexes to names
    for i in range(len(student_nodes)):
        ref_dict[student_nodes[i]] = i+1
    s_end = len(student_nodes)+1
    for i in range(len(class_nodes)):
        ref_dict[class_nodes[i]] = i + s_end
    end_len = len(ref_dict)
    ref_dict['t'] = end_len

    total_nodes = len(ref_dict)
    for i in range(total_nodes):
        graph.append([])
        for j in range(total_nodes):
            graph[i].append(0)

    #connect start node to every student
    for i in student_nodes:
        graph[0][ref_dict[i]] = n
    
    #connect students to courses
    for i in want_list:
        graph[ref_dict[i[0].rstrip()]][ref_dict[i[1].rstrip()]] = 1
    
    #connect courses to terminal
    for i in cap_list:
        graph[ref_dict[i[0].rstrip()]][total_nodes-1] = int(i[1])

    return graph

def studentList(want_list):
    students = set()
    for item in want_list:
        students.add(item[0])
    return list(students)

def classList(cap_list):
    classes = []
    for item in cap_list:
        classes.append(item[0].rstrip())
    return classes
    
if __name__ == "__main__":
    #First line is 3 numbers r, c, n
    #Scan first r lines
    #Scan next c lines
    #if all 3 are 0, terminate
    r = 0 
    c = 0
    n = 0
    want_list = []
    cap_list = []
    
    for line in sys.stdin:

        if not line.rstrip():
            continue

        line = line.split(' ')

        if (r + c) == 0: #Assumption: r or c CANNOT be negative
            if len(want_list) > 0:
                print(scheduleCheck(want_list, cap_list, n))
                want_list = []
                cap_list = []
            r = int(line[0])
            c = int(line[1])
            n = int(line[2])
            continue
        
        if (r + c + n) == 0:
            break
        
        if r > 0:
            want_list.append(line)
            r-=1
        elif c > 0:
            cap_list.append(line)
            c-=1
        

