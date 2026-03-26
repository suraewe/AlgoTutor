import collections
import heapq
import time
import os
import sys

MAZE = [
    ['.', '.', '.', '.', '.'],
    ['.', '#', '#', '.', '.'],
    ['.', '#', '.', '.', '.'],
    ['.', '.', '.', '#', '.'],
    ['.', '.', '.', '.', 'G'],
]
START = (0, 0)
GOAL  = (4, 4)

ROWS = len(MAZE)
COLS = len(MAZE[0])

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BLUE   = "\033[94m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

CELL_COLORS = {
    'S': GREEN  + BOLD,
    'G': RED    + BOLD,
    '#': "\033[90m",
    '.': "\033[37m",
    '*': YELLOW,
    '@': CYAN   + BOLD,
}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_maze(grid, visited=None, path=None, title=""):
    visited = visited or set()
    path    = path    or []
    path_set = set(path)

    print(f"\n{BOLD}{title}{RESET}")
    print("  " + " ".join(str(c) for c in range(COLS)))

    for r in range(ROWS):
        row_str = f"{r} "
        for c in range(COLS):
            cell = MAZE[r][c]
            pos  = (r, c)

            if pos == START:
                ch = CELL_COLORS['S'] + "S" + RESET
            elif pos == GOAL:
                ch = CELL_COLORS['G'] + "G" + RESET
            elif pos in path_set and pos not in (START, GOAL):
                ch = CELL_COLORS['@'] + "@" + RESET
            elif pos in visited and cell != '#':
                ch = CELL_COLORS['*'] + "*" + RESET
            else:
                color = CELL_COLORS.get(cell, RESET)
                ch = color + cell + RESET

            row_str += ch + " "
        print(row_str)

    print(f"\n  {GREEN}S{RESET}=Start  {RED}G{RESET}=Goal  {DIM}#{RESET}=Wall  "
          f"{YELLOW}*{RESET}=Visited  {CYAN}@{RESET}=Path\n")

def get_neighbors(pos):
    r, c = pos
    moves = [(-1,0,'Up'), (1,0,'Down'), (0,-1,'Left'), (0,1,'Right')]
    result = []
    for dr, dc, direction in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and MAZE[nr][nc] != '#':
            result.append(((nr, nc), direction))
    return result

def reconstruct_path(came_from, start, goal):
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

def manhattan(pos, goal=GOAL):
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

def pause(msg="Press enter to continue..."):
    input(f"{DIM}{msg}{RESET}")


def bfs(animate=True, delay=0.4):
    header = "[ Breadth-First Search (BFS) ]"

    queue     = collections.deque([START])
    visited   = {START}
    came_from = {START: None}
    step      = 0

    print_maze([], visited=set(), title=header + " - Initial Maze")
    pause()

    while queue:
        current = queue.popleft()
        step += 1

        if animate:
            clear()
            print_maze([], visited=visited,
                       title=f"{header} - Step {step} | Checking {current}")
            print(f"  Queue size: {len(queue)+1} | Visited: {len(visited)}")
            time.sleep(delay)

        if current == GOAL:
            path = reconstruct_path(came_from, START, GOAL)
            clear()
            print_maze([], visited=visited, path=path,
                       title=f"{header} - Path found in {step} steps.")
            print(f"  Shortest path: {len(path)-1} moves\n")
            return path

        for (neighbor, direction) in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)

    print("  No path found.")
    return []


def dfs(animate=True, delay=0.4):
    header = "[ Depth-First Search (DFS) ]"

    stack     = [START]
    visited   = set()
    came_from = {START: None}
    step      = 0

    print_maze([], visited=set(), title=header + " - Initial Maze")
    pause()

    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        step += 1

        if animate:
            clear()
            print_maze([], visited=visited,
                       title=f"{header} - Step {step} | Checking {current}")
            print(f"  Stack size: {len(stack)} | Visited: {len(visited)}")
            time.sleep(delay)

        if current == GOAL:
            path = reconstruct_path(came_from, START, GOAL)
            clear()
            print_maze([], visited=visited, path=path,
                       title=f"{header} - Path found in {step} steps.")
            print(f"  Path length: {len(path)-1} moves (Not always shortest)\n")
            return path

        for (neighbor, _) in get_neighbors(current):
            if neighbor not in visited:
                came_from[neighbor] = current
                stack.append(neighbor)

    print("  No path found.")
    return []


def greedy(animate=True, delay=0.4):
    header = "[ Greedy Best-First Search ]"

    heap      = [(manhattan(START), START)]
    visited   = set()
    came_from = {START: None}
    step      = 0

    print_maze([], visited=set(), title=header + " - Initial Maze")
    pause()

    while heap:
        h_cost, current = heapq.heappop(heap)

        if current in visited:
            continue
        visited.add(current)
        step += 1

        if animate:
            clear()
            print_maze([], visited=visited,
                       title=f"{header} - Step {step} | Checking {current} (h={h_cost})")
            print(f"  Frontier: {len(heap)} | Visited: {len(visited)}")
            time.sleep(delay)

        if current == GOAL:
            path = reconstruct_path(came_from, START, GOAL)
            clear()
            print_maze([], visited=visited, path=path,
                       title=f"{header} - Path found in {step} steps.")
            print(f"  Path length: {len(path)-1} moves (Not always optimal)\n")
            return path

        for (neighbor, _) in get_neighbors(current):
            if neighbor not in visited:
                came_from[neighbor] = current
                heapq.heappush(heap, (manhattan(neighbor), neighbor))

    print("  No path found.")
    return []


def astar(animate=True, delay=0.4):
    header = "[ A* Search ]"

    heap      = [(0 + manhattan(START), 0, START)]
    visited   = set()
    came_from = {START: None}
    g_score   = {START: 0}
    step      = 0

    print_maze([], visited=set(), title=header + " - Initial Maze")
    pause()

    while heap:
        f, g, current = heapq.heappop(heap)

        if current in visited:
            continue
        visited.add(current)
        step += 1

        if animate:
            clear()
            h = manhattan(current)
            print_maze([], visited=visited,
                       title=f"{header} - Step {step} | {current} | g={g} h={h} f={g+h}")
            print(f"  Frontier: {len(heap)} | Visited: {len(visited)}")
            time.sleep(delay)

        if current == GOAL:
            path = reconstruct_path(came_from, START, GOAL)
            clear()
            print_maze([], visited=visited, path=path,
                       title=f"{header} - Goal reached in {step} steps.")
            print(f"  Optimal path length: {len(path)-1}\n")
            return path

        for (neighbor, _) in get_neighbors(current):
            new_g = g + 1 
            if neighbor not in visited and new_g < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = new_g
                came_from[neighbor] = current
                heapq.heappush(heap, (new_g + manhattan(neighbor), new_g, neighbor))

    print("  No path found.")
    return []


def bfs_walkthrough():
    print(f"\n{'-'*50}")
    print("  Step-by-Step BFS Guide")
    print(f"{'-'*50}")
    print("""
Grid layout:
   0 1 2 3 4
0  S . . . .
1  . # # . .
2  . # . . .
3  . . . # .
4  . . . . G

Start is (0,0), Goal is (4,4).
Walls are at: (1,1), (1,2), (2,1), (3,3).

BFS uses a Queue to explore layer by layer.
""")

    steps = [
        ("Start", "Queue: [(0,0)]", "Visited: (0,0)",
         "Put the starting cell in the queue."),
        ("Step 1", "Pop (0,0) -> check neighbors", "Add (0,1), (1,0)",
         "Pop current element from the front. Its neighbors are (0,1) and (1,0). Add both to queue."),
        ("Step 2", "Pop (0,1) -> check neighbors", "Add (0,2)",
         "Next is (0,1). Right is (0,2), down is a wall, left was already visited. Add (0,2)."),
        ("Step 3", "Pop (1,0) -> check neighbors", "Add (2,0)",
         "Next is (1,0). Up is visited, down is (2,0), right is a wall. Add (2,0)."),
        ("...", "", "",
         "This continues level by level until the goal is found."),
        ("Done", "Final path found", "",
         "Once goal is hit, we follow the pointers back to the start."),
    ]

    for title, queue_state, extra, explanation in steps:
        print(f"  {BOLD}{title}{RESET}")
        if queue_state: print(f"    {queue_state}")
        if extra:       print(f"    {extra}")
        print(f"    {explanation}\n")

    pause()


def print_summary():
    print(f"\n{'-'*50}")
    print("  Algorithm Comparison")
    print(f"{'-'*50}\n")

    rows = [
        ("BFS", "Queue", "Yes", "Medium", "Lots of memory"),
        ("DFS", "Stack", "No", "Fast*", "Goes deep, can miss shorter paths"),
        ("Greedy", "Heuristic", "No", "Fast", "Easily fooled by obstacles"),
        ("A*", "g + h", "Yes", "Fast", "Calculated and efficient"),
    ]

    header = f"{'Algorithm':<10} {'Data Struct':<16} {'Shortest?':<10} {'Speed':<8} {'Note'}"
    print(f"  {BOLD}{header}{RESET}")
    print("  " + "-" * 70)
    for r in rows:
        print(f"  {r[0]:<10} {r[1]:<16} {r[2]:<10} {r[3]:<8} {r[4]}")

    print("\n  Closing Thoughts:")
    print("  - BFS is reliable but slow.")
    print("  - A* is usually the best bet for pathfinding.")
    print("  - Greedy is fast but might take a weird route.\n")


def main():
    options = {
        "1": ("BFS (Breadth-First Search)", bfs),
        "2": ("DFS (Depth-First Search)", dfs),
        "3": ("Greedy Search", greedy),
        "4": ("A*", astar),
        "5": ("BFS Text Guide", bfs_walkthrough),
        "6": ("Algorithm Comparison Table", print_summary),
        "7": ("Run Everything", None),
        "0": ("Exit", None),
    }

    while True:
        clear()
        print(f"""
{BOLD}=========================================
      Maze Solver / Algo Tutor
========================================={RESET}

Legend: {GREEN}S{RESET}=Start {RED}G{RESET}=Goal {DIM}#{RESET}=Wall {YELLOW}*{RESET}=Visited {CYAN}@{RESET}=Path
""")
        print_maze([], title="Current Grid")
        print("Menu options:\n")
        for key, (label, _) in options.items():
            print(f"  [{key}] {label}")
        print()

        choice = input("Your choice: ").strip()

        if choice == "0":
            print("\nGoodbye!\n")
            break
        elif choice == "7":
            for key in ["1", "2", "3", "4"]:
                clear()
                _, fn = options[key]
                fn(animate=True, delay=0.2)
                pause(f"  Done with {options[key][0]}. Press enter for next...")
            print_summary()
            pause()
        elif choice in options:
            label, fn = options[choice]
            if fn:
                clear()
                fn() if choice in ("5", "6") else fn(animate=True, delay=0.3)
                pause()
        else:
            print("Not a valid option.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nStopped by user. Exiting.")
        sys.exit(0)
        
