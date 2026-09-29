# Assignment 2 — State-Space Search

A C++ solution to a constrained river-crossing problem. Each state records the number of explorers and guardians on one side of the river, the boat location, and a parent state. Breadth-first search explores valid states and reconstructs an optimal sequence of crossings once the goal is reached.

## Concepts

- Breadth-first search (BFS)
- Explicit state-space representation
- Constraint checking
- Visited-state tracking
- Parent pointers and optimal-path reconstruction

## Build and run

```bash
g++ src/main.cpp -o state_space_search
./state_space_search
```
