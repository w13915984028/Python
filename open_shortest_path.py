
class Edge:
    def __init__(self, s = 0, e = 0, w = 0):
        self._start = s
        self._end = e
        self._weight = w

    def start(self):
        return self._start

    def end(self):
        return self._end

    def weight(self):
        return self._weight

    def __str__(self):
        return "(Edge: start:"+str(self._start)+" end:"+str(self._end)+" weight:"+str(self._weight)+")"

    def __repr__(self):
        return self.__str__()


class Node:
    def __init__(self, idx = 0, d = 0, p = -1):
        self._idx = idx
        self._distance = d
        self._parent = p

    def idx(self):
        return self._idx

    def distance_get(self):
        return self._distance

    def distance_set(self, d):
        self._distance =d 

    def parent_get(self):
        return self._parent

    def parent_set(self, p):
        self._parent = p

    def __str__(self):
        return "(Node: id:"+str(self._idx)+" distance:"+str(self._distance)+" parent:"+str(self._parent)+")"

    def __repr__(self):
        return self.__str__()

# priority node, for Heap or other usage
class PriorityNode:
    def __init__(self, idx=0, prio=0):
        self._idx = idx
        self._priority = prio

    def idx(self):
        return self._idx

    def priority(self):
        return self._priority

def add_new_to_list(stk, nd):
    stk.append(nd)

# save (node, distance) pare; can be list or queue or heap or any...
def add_new_to_container(c, nd):
    add_new_to_list(c, nd)

def get_min_from_list(lst):
    if lst is None:
        return None

    idx = 0
    i = 1
    while i < len(lst):
        if lst[i].priority() < lst[idx].priority():
            idx = i
        i += 1
    # get min and remove it from list
    ret = lst[idx]
    lst.pop(idx)
    return ret

def get_min_from_container(c):
    return get_min_from_list(c)

def print_distance(nodes):
    i = 1
    while i <len(nodes):
        print("vertex:", i, "distance:", nodes[i].distance_get(), "parent:", nodes[i].parent_get())
        i += 1    

def print_path(start, end, nodes):
    pth = [end]

    np = nodes[end].parent_get()
    while np != start:       
        pth.append(np)
        np = nodes[np].parent_get()

    pth.append(start)
    print("shortest path from end to start:", pth)

def shortest_path(node_cnt, edges, nodes, start, end):
    stk = []
    add_new_to_container(stk, PriorityNode(start, 0))

    nodes[start].distance_set(0)
    nodes[start].parent_set(0)    #start point

    state =  [-1 for x in range(0, node_cnt + 1)] # -1: unvisited; 0: found
    state[start] = 0 # found

    while len(stk) > 0:
        mm = get_min_from_container(stk) # get min
        if mm is None:
            break

        # find neighbour 
        for x in edges:
            found = False
            if x.start() == mm.idx():
                ss = x.start()
                ee = x.end()
                ww = x.weight()
                found = True
                # check x[1]
            elif x.end() == mm.idx():
                ss = x.end()
                ee = x.start()
                ww = x.weight()
                found = True

            if found is True:
                # is neighbour

                # update parent and distance
                if nodes[ss].distance_get() + ww < nodes[ee].distance_get():
                    nodes[ee].distance_set( nodes[ss].distance_get() + ww ) # new shorter path
                    nodes[ee].parent_set(ss) # set ee's parentas ss
                    # print(" update distance:", ee, nodes[ee].distance_get())

                if state[ee] == -1: # not visit yet
                    # print("found new:", ss, ee, nodes[ee].distance_get())
                    add_new_to_container(stk, PriorityNode(ee, nodes[ee].distance_get()))
                    state[ee] = 0 # visited

    #finally, print them
    print_distance(nodes)
    print_path(start, end, nodes)

if __name__ == "__main__":
    print("open shortest path")

    node_cnt = 8

    # parent as -1; distance as a big value
    nodes = [Node(x, 0xffff, -1) for x in range(0, node_cnt + 1)]

    edges = [Edge(1,2,4), Edge(1,3,3), Edge(2,4,3), Edge(2,5,1), Edge(3,5,4), Edge(3,6,4), Edge(4,7,3), Edge(5,7,2), Edge(6,7,2), Edge(5,6,1), Edge(4,8,3), Edge(7,8,2)]

    shortest_path(node_cnt, edges, nodes, 1, 8)

	# if needs find other (start, end)
    #  then, all nodes[xx].distance & parent needs to be reset to initial value

'''
                   / 8
               /(3)  |
             4       |
         (3)/ \    (2)
       2 /     \     |
      / \       \    |
   (4)    (1)   (3)  |
  /        \       \ |
1           5--(2)---7
 \         /\        |
  (3)  (4)/  \       |
     \  /     \      |
      3       (1)    |
       \        \   (2)
        \(4)     \   |
         \-----   \  6
     

'''



'''
# start 1, end 8
# the node & distance update process

('vertex:', 1, 'distance:', 0, 'parent:', 0)
('vertex:', 2, 'distance:', 4, 'parent:', 1)
('vertex:', 3, 'distance:', 3, 'parent:', 1)
('vertex:', 4, 'distance:', 7, 'parent:', 2)
('vertex:', 5, 'distance:', 5, 'parent:', 2)
('vertex:', 6, 'distance:', 6, 'parent:', 5)
('vertex:', 7, 'distance:', 7, 'parent:', 5)
('vertex:', 8, 'distance:', 9, 'parent:', 7)
('shortest path from end to start:', [8, 7, 5, 2, 1])

'''
