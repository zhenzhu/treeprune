# treeprune 

**treeprune.py** is a Python module that provides a network-pruning functionality
and returns a tree with the customized root node, edge weight threshold, 
maximum number of layers, and search direction. 

This project is hosted at: [https://github.com/zhenzhu/treeprune](https://github.com/zhenzhu/treeprune).

MIT License

Copyright (c) 2016 Zhen Zhu

<hr>

**Table of Contents**
- [Usage](#usage)
	- [Download](#download)
	- [Input](#input)
	- [Functions](#functions)
- [Testing](#testing)
- [Reference](#reference)
- [Acknowledgements](#acknowledgements)

<hr>
**Packages Required:**
- [networkx](https://networkx.github.io/)
- [pygraphviz](https://pygraphviz.github.io/)

<br>

# Usage
[[back to top](#treeprune)]

## Download
The easiest way is to download the script **treeprune.py** directly:

1. Go to the raw version of [treeprune.py](https://github.com/zhenzhu/treeprune/raw/master/treeprune.py).
2. Right click and save it. 

## Input

**treeprune.py** only works with directed and weighted networks.

An edge list file is needed as an input. The file should be formatted as:

```
a,b,0.17
b,c,0.54
...,...,...
```

The implicit header, from left to right, is **source**, **target**, and **edge weight**.

In this example, comma is used as the delimiter. You may choose a different
delimiter, so please always specify your delimiter when using the function
`get_tree` below.

## Functions

Two functions are available:

1. `get_tree` takes the path of a data file of edge list with numeric 
    weights and returns a tree (`DiGraph` object). The parameters include:  
	* `data_path`: The path of a data file of edge list with numeric weights.
    * `sep`: The delimiter of the data file. 
    * `root`: A root node to start with. 
    * `cutoff`: The edge weight threshold. 
    * `layer_max`: The number of layers to explore.
    * `up`: The direction (upstream or downstream) of the tree. The default is upstream.

2. `plot_tree` returns a tree plot. The parameters include:
    * `tree`: A tree (`DiGraph` object).
    * `fig_path`: A string of the path saving the plot. 
    * `layer_space`: A parameter controlling the space between layers. The default is 3.
    * `edge_color`: A string of edge color. The default is 'crimson'.

<br>

# Testing
[[back to top](#treeprune)]

An example edge list file can be downloaded from the following link, [https://raw.githubusercontent.com/zhenzhu/treeprune/master/examples/exampleEdgeList.csv](https://raw.githubusercontent.com/zhenzhu/treeprune/master/examples/exampleEdgeList.csv).

```python
import treeprune as tp

myPath = './exampleEdgeList.csv' 
# Please replace the first dot with your local path. 

myTree = tp.get_tree(data_path=myPath, sep=',', root='a', cutoff='0.2', layer_max=3, up=False)
# sep=',' because comma is the delimiter in exampleEdgeList.csv.
# up=False makes the search downstream. 

tp.plot_tree(myTree, 'test.png')
```

The code is working properly if the figure at the following link is returned, [https://github.com/zhenzhu/treeprune/blob/master/examples/test.png](https://github.com/zhenzhu/treeprune/blob/master/examples/test.png).


<br>

# Reference
[[back to top](#treeprune)]

If using the code, please cite the publication below:

Zhu Z, Puliga M, Cerina F, Chessa A, Riccaboni M (2015) 
[Global Value Trees](http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0126699). PLoS ONE 10(5): e0126699. 
doi:10.1371/journal.pone.0126699

# Acknowledgements
[[back to top](#treeprune)]

Special thanks go to Michelangelo Puliga and Juan Ignacio Perotti for their
superb tutorials on Python and Git and inspiring conversations. 


