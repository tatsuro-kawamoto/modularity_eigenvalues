# modularity_eigenvalues
Estimate the number of communities from the spectrum of the modularity matrix.

This program computes the leading eigenvalues of the modularity matrix [1]. 
This program also computes a mean-field estimate [2] of its spectral band edge.
The number of eigenvalues outside of the spectral band (+1) gives the number of statistically significant communities.

## Requird python packages
- numpy
- scipy
- matplotlib
- docopt

## USAGE
Following command returns the number of communities: 
```
eigs.py edgelist.txt
```
`edgelist.txt` is the edgelist that indicates an undirected unweighted graph, e.g., 
```
0 1
1 2
2 3
...
```

## OPTIONS
- Major options:
  - k: Max. of the number of communities [default: 10]
  - resolution: Resolution parameter [default: 1]
- Minor options:
  - zup: Upper bound of variable z [default: 100]
  - zlow: Lower bound of variable z [default: 1]

The range of z has to be specified in order to find a root in the estimate of the spectral band edge.

## References
[1] M.E.J. Newman, Proc. Natl. Acad. Sci. U.S.A., 103 8577 (2006).

[2] T. Kawamoto and Y. Kabashima, Europhys. Lett., 112 40007 (2015).
