# graph-infecter
Infect a colored network within the max amount of iterations (or a script to solve Kami puzzles).

## Rules
- A vertex can only be infected with a different color.
- Once the vertex is infected, neighbours with the same color are merged into the infected node.
- The minimum ID is kept to represent this new node.

The objective is to infect all vertices in an optimized way, constrained to a max number of movements (infections).

## Example
<p align="center">
  <img width="500" height="500" src="/resources/example_solution.gif">
</p>

## Input files
The input file for the previous example is available at: `/input/pati.txt`. It follows the following format:
```
int: number_of_vertices
int: movements (int)
string: whitespace separated list of colors
int: color id of vertex 0
...
int: color id of vertex number_of_vertices - 1
int int: start & end vertices of connection 0
...
int int: start & end vertices of connection n_connections - 1
```

Example:
```
5
2
red blue green
2
1
1
0
0
1 2
1 3
2 4
3 5
```
This will set the following graph:
<p align="center">
  <img width="450" height="450" src="/resources/small_input.jpeg">
</p>

# TODO
- [ ] Make program completely zero-based. Currently the labels start with 1, which complicates the code.
- [ ] Pass input file as argument to the script. 
