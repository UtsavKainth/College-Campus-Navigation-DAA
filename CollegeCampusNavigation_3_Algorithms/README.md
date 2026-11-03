# College Campus Navigation System

MCA Design and Analysis of Algorithms mini project, written in beginner-friendly Python.

## How to run

1. Install Python 3 with Tkinter support.
2. Open this folder in VS Code.
3. Open the VS Code terminal.
4. Run `python main.py` (or `py main.py` on Windows).

No pip packages are required.

## Three algorithms

- **Dijkstra:** Finds the shortest path between selected campus locations using a simple linear search for the next vertex. Time complexity: O(V² + E).
- **Kruskal:** Sorts edges and adds them if they do not create a cycle. This implementation uses a simple parent array without path compression; sorting costs O(E log E), and the repeated find operations can cost O(EV).
- **Bubble Sort:** Sorts destinations by their shortest walking distances from the selected starting location. Time complexity: O(V²) for the sorting step.

## Viva notes

- Graph: a collection of vertices (campus places) and edges (walking paths).
- Edge weight: walking distance in metres.
- Dijkstra: shortest path between two locations; requires nonnegative edge weights.
- Minimum spanning tree (MST): connects every location with no cycles and minimum total network distance.
- Kruskal: selects cheap edges and avoids cycles.
- Bubble Sort: swaps neighbouring values when they are out of order.
- Kruskal solves a different problem from Dijkstra: it minimizes total network distance, not necessarily the shortest journey between two places.

## Notes

All distances and map positions are illustrative, not a survey of a real college campus. The application is an educational simulation, not a live navigation service.
