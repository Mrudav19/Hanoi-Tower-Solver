import time
import heapq as hq

class HanoiTowerNode:
    def __init__(self, disks, depth=0, heuristic=0):
        self.disks = disks
        self.depth = depth
        self.heuristic = heuristic
        self.parent = None

    def printDisks(self):
        for i, peg in enumerate(self.disks):
            disks = ", ".join(str(disk) for disk in peg)
            print(f"Peg {i + 1}: {disks}")
        print()

    def generateChildren(self):
        children = []
        for i in range(len(self.disks)):
            if len(self.disks[i]) > 0:
                for j in range(len(self.disks)):
                    if i != j and (len(self.disks[j]) == 0 or self.disks[i][-1] < self.disks[j][-1]):
                        child_disks = [peg.copy() for peg in self.disks]
                        disk = child_disks[i].pop()
                        child_disks[j].append(disk)
                        heuristic = self.calculateHeuristic(child_disks)
                        child = HanoiTowerNode(child_disks, self.depth + 1, heuristic)
                        child.parent = self
                        children.append(child)
        return children

    def isGoalState(self):
        return self.disks == [[], [], [5, 4, 3, 2, 1]]

    def calculateHeuristic(self, disks):
        goal_peg = [5, 4, 3, 2, 1]
        misplaced_disks = 0
        for i in range(len(disks)):
            for j in range(len(disks[i])):
                if disks[i][j] != goal_peg[j]:
                    misplaced_disks += 1
        return misplaced_disks

    def __lt__(self, other):
        return (self.depth + self.heuristic) < (other.depth + other.heuristic)


class HanoiTowerSearch:
    def __init__(self):
        pass

    def depthFirstSearch(self, root):
        visited = set()
        stack = [root]

        while stack:
            current_node = stack.pop()
            if current_node.isGoalState():
                return current_node

            visited.add(tuple(map(tuple, current_node.disks)))

            children = current_node.generateChildren()
            for child in children:
                if tuple(map(tuple, child.disks)) not in visited:
                    stack.append(child)

        return None

    def aStarSearch(self, root):
        visited = set()
        heap = []
        hq.heappush(heap, root)

        while heap:
            current_node = hq.heappop(heap)
            if current_node.isGoalState():
                return current_node

            visited.add(tuple(map(tuple, current_node.disks)))

            children = current_node.generateChildren()
            for child in children:
                if tuple(map(tuple, child.disks)) not in visited:
                    hq.heappush(heap, child)

        return None

    def getPath(self, node):
        path = []
        current = node
        while current:
            path.append(current)
            current = current.parent
        path.reverse()
        return path


if __name__ == "__main__":
    initial_disks = [[5, 4, 3, 2, 1], [], []]
    goal_disks = [[], [], [5, 4, 3, 2, 1]]
    root = HanoiTowerNode(initial_disks)

    print("Welcome to the Hanoi Tower Solver!")
    print("=================================")
    print()

    print("Initial State:")
    root.printDisks()

    print("Goal State:")
    for i, peg in enumerate(goal_disks):
        disks_str = ", ".join(str(disk) for disk in peg)
        print(f"Peg {i + 1}: {disks_str}")
    print()

    print("Finding Solution (DFS):")
    dfs_start_time = time.time()
    dfs_search = HanoiTowerSearch()
    dfs_solution = dfs_search.depthFirstSearch(root)
    dfs_end_time = time.time()
    if dfs_solution:
        print("By employing depth-first search, a solution is found:")
        print("=============================")
        for i, node in enumerate(dfs_search.getPath(dfs_solution)):
            print(f"Step {i + 1}:")
            node.printDisks()
        print("To solve the Hanoi Tower, the number of steps required:", dfs_solution.depth)
        print("Time Taken:", dfs_end_time - dfs_start_time, "seconds")
    else:
        print("Unfortunately, we have been unable to find a way to solve the problem.")

    print("\nFinding Solution (A*):")
    astar_start_time = time.time()
    astar_search = HanoiTowerSearch()
    astar_solution = astar_search.aStarSearch(root)
    astar_end_time = time.time()
    if astar_solution:
        print("By employing A* search, a solution is found:")
        print("===================")
        for i, node in enumerate(astar_search.getPath(astar_solution)):
            print(f"Step {i + 1}:")
            node.printDisks()
        print("To solve the Hanoi Tower, the number of steps required:", astar_solution.depth)
        print("Time Taken:", astar_end_time - astar_start_time, "seconds")
    else:
        print("Unfortunately, we have been unable to find a way to solve the problem.")
        
    print("\nThank you for using the Hanoi Tower Solver. Have a great day!")
