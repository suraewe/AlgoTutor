# AlgoTutor

Just a simple Python script I put together to visualize how different search algorithms work on a maze. It's mostly for learning BFS, DFS, and A* without having to read through a whole textbook.

 What's in here?
- BFS: Finds the shortest path, but explored a lot of cells.
- DFS: Fast, but doesn't always find the best route.
- Greedy: Uses a heuristic to guess the way.
- A*: The best one—fast and finds the shortest path.

- How to run it
You just need Python installed. No extra libraries required because I used `collections` and `heapq` from the standard library.

- How it works
The maze is just a 2D list in the code. `.` are paths, `#` are walls, `S` is the start, and `G` is the goal. When you run an algorithm, it'll animate the search in your terminal so you can see how the queue or stack grows.

I added a "Run Everything" option if you just want to see them all go back-to-back.

- Notes
- Works best in a terminal that supports ANSI colors (most do these days).
- If you want to change the maze, just edit the `MAZE` list at the top of the script.

