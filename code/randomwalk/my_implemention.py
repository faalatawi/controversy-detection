import networkx as ns
from networkx import Graph
import random
import sys
from typing import Dict, Any, List
from enum import Enum, auto


class LabelType(Enum):
    LEFT = auto()
    RIGHT = auto()
    BOTH = auto()


def get_random_nodes(G: Graph, k: int) -> Dict[Any, int]:
    """ 
    get random nodes

    # Attributes
    - `G` : A networkx graph
    - `k` : number (`int`) of random nodes to generate

    # Output
    A dictionary of node ids and int always = 1. Example: 
    ```python
    {'node1' : 1, 'node2' : 1} 
    ```
    """
    nodes = G.nodes()
    random_nodes = {}

    for _ in range(k):
        random_id = random.randint(0, len(nodes)-1)
        random_nodes[nodes[random_id]] = 1

    return random_nodes


def get_random_nodes_from_labels(left: List, right: List, k: int, flag: LabelType) -> Dict[Any, int]:
    """
    Get a k random nodes from left or right or both 
    ## Attributes
    - `G` : A networkx graph
    - `k` : number (`int`) of random nodes to generate
    - `flag` : could be `LabelType.LEFT`, `LabelType.RIGHT` or `LabelType.BOTH`

    ## Output
    A dictionary of node ids and an int always = 1. Example: 
    ```python
    {'node1' : 1, 'node2' : 1} 
    ```
    """
    random_nodes = {}

    both = flag == LabelType.BOTH
    if both:
        # If both, k/2 from one side and k/2 from the other side are generated.
        k /= 2

    if flag == LabelType.LEFT or both:
        for _ in range(k):
            random_id = random.randint(0, len(left) - 1)
            random_nodes[left[random_id]] = 1

    if flag == LabelType.RIGHT or both:
        for _ in range(k):
            random_id = random.randint(0, len(right) - 1)
            random_nodes[right[random_id]] = 1

    return random_nodes


def get_nodes_from_labels_with_highest_degree(G, dict_left, dict_right, k: int, flag: LabelType) -> Dict[Any, int]:
    random_nodes = {}

    # Find High degree
    dict_degrees_left = {}
    dict_degrees_right = {}

    for node in G.nodes():

        if node in dict_left:
            dict_degrees_left[node] = G.degree(node)

        if node in dict_right:
            dict_degrees_right[node] = G.degree(node)
    #! fixme
    dict_degrees_left = sorted(dict_degrees_left.items(), key=itemgetter(
        1), reverse=True)  # sorts nodes by degrees
    dict_degrees_right = sorted(dict_degrees_right.items(), key=itemgetter(
        1), reverse=True)  # sorts nodes by degrees

    both = flag == LabelType.BOTH
    if both:
        # If both, k/2 from one side and k/2 from the other side are generated.
        k /= 2

    if flag == LabelType.LEFT or both:
        random_nodes += dict_degrees_right[:k]

    if flag == LabelType.RIGHT or both:
        random_nodes += dict_degrees_right[:k]

    return random_nodes


if __name__ == "__main__":
    flag = False

    r = range(0, 10)
    if flag:
        r = range(0, 10, 2)

    for i in r:
        print(i)
