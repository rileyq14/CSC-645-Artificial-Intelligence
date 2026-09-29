# Assignment 1 — Vacuum Agent

A C++ implementation of a simple vacuum-cleaner agent operating across a configurable number of rooms. The program evaluates the agent across every combination of starting location and clean/dirty room configuration, records each score, and reports aggregate performance.

## Concepts

- Agent/environment separation
- Percept-driven action selection
- State transitions
- Performance measurement
- Exhaustive configuration testing

## Build and run

```bash
g++ src/main.cpp src/agent.cpp src/environment.cpp -o vacuum_agent
./vacuum_agent
```

Enter the number of rooms when prompted.
