from sys import maxsize
from queue import PriorityQueue
from time import time
class Puzzle:
    #تعریف حالت نهایی و مقدار دهی اولیه 
    goal_state=[1,2,3,4,5,6,7,8,0]
    heuristic=None
    evaluation_function=None
    needs_hueristic=False
    num_of_instances=0
    #تشکیل پازل و حالتهای پدر و فرزند و تابع هیورستیک
    def __init__(self,state,parent,action,path_cost,needs_hueristic=False):
        self.parent=parent
        self.state=state
        self.action=action
        if parent:
            self.path_cost = parent.path_cost + path_cost
        else:
            self.path_cost = path_cost
        if needs_hueristic:
            self.needs_hueristic=True
            self.generate_heuristic()
            self.evaluation_function=self.heuristic+self.path_cost
        Puzzle.num_of_instances+=1
    #نمایش حالت
    def __str__(self):
        return str(self.state[0:3])+'\n'+str(self.state[3:6])+'\n'+str(self.state[6:9])
    #تعریف هیورستیک با منهتن دیستنس
    def generate_heuristic(self):
        self.heuristic=0
        for num in range(1,9):
            distance=abs(self.state.index(num) - self.goal_state.index(num))
            i=int(distance/3)
            j=int(distance%3)
            self.heuristic=self.heuristic+i+j
    #ازمون هدف
    def goal_test(self):
        if self.state == self.goal_state:
            return True
        return False
    #تابع برای اینکه برای هر خانه موقع حرکت از محدوده خارج نشوند و در محیط 3* 3بمانند
    @staticmethod
    def find_legal_actions(i,j):
        legal_action = ['U', 'D', 'L', 'R']
        if i == 0:
            legal_action.remove('U')
        elif i == 2:
            legal_action.remove('D')
        if j == 0:
            legal_action.remove('L')
        elif j == 2:
            legal_action.remove('R')
        return legal_action
    #پیداکردن تمام حالتهای فرزند تا در تابع بعدی با تابع هیورستیک جواب را بتواند پیدا کند
    def generate_child(self):
        children=[]
        x = self.state.index(0)
        i = int(x / 3)
        j = int(x % 3)
        legal_actions=self.find_legal_actions(i,j)

        for action in legal_actions:
            new_state = self.state.copy()
            if action == 'U':
                new_state[x], new_state[x-3] = new_state[x-3], new_state[x]
            elif action == 'D':
                new_state[x], new_state[x+3] = new_state[x+3], new_state[x]
            elif action == 'L':
                new_state[x], new_state[x-1] = new_state[x-1], new_state[x]
            elif action == 'R':
                new_state[x], new_state[x+1] = new_state[x+1], new_state[x]
            children.append(Puzzle(new_state,self,action,1,self.needs_hueristic))
        return children

    def find_solution(self):
        solution = []
        solution.append(self.action)
        path = self
        while path.parent != None:
            path = path.parent
            solution.append(path.action)
        solution = solution[:-1]
        solution.reverse()
        return solution
def Astar_search(initial_state):
    count=0
    explored=[]
    start_node=Puzzle(initial_state,None,None,0,True)
    q = PriorityQueue()
    q.put((start_node.evaluation_function,count,start_node))

    while not q.empty():
        node=q.get()
        node=node[2]
        explored.append(node.state)
        if node.goal_test():
            return node.find_solution()

        children=node.generate_child()
        for child in children:
            if child.state not in explored:
                count += 1
                q.put((child.evaluation_function,count,child))
    return
def recursive_best_first_search(initial_state):
    node=RBFS_search(Puzzle(state=initial_state, parent=None, action=None, path_cost=0, needs_hueristic=True), f_limit=maxsize)
    node=node[0]
    return node.find_solution()

def RBFS_search(node,f_limit):
    successors=[]

    if node.goal_test():
        return node,None
    children=node.generate_child()
    if not len(children):
        return None, maxsize
    count=-1
    for child in children:
        count+=1
        successors.append((child.evaluation_function,count,child))
    while len(successors):
        successors.sort()
        best_node=successors[0][2]
        if best_node.evaluation_function > f_limit:
            return None, best_node.evaluation_function
        alternative=successors[1][0]
        result,best_node.evaluation_function=RBFS_search(best_node,min(f_limit,alternative))
        successors[0]=(best_node.evaluation_function,successors[0][1],best_node)
        if result!=None:
            break
    return result,None
state=[]
print("enter 0 to 9 to solve:")
for i in range(0,9):
    n=int(input())
    state.append(n)
for i in range(0,1):

    Puzzle.num_of_instances = 0
    t0 = time()
    astar = Astar_search(state)
    t1 = time() - t0
    print('A*:',astar)
    print('space:', Puzzle.num_of_instances)
    print('time:', t1)
    print()

    Puzzle.num_of_instances = 0
    t0 = time()
    RBFS = recursive_best_first_search(state)
    t1 = time() - t0
    print('RBFS:',RBFS)
    print('space:', Puzzle.num_of_instances)
    print('time:', t1)
    print()

    print('------------------------------------------')