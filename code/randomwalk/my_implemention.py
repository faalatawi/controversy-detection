import networkx as nx
from networkx import Graph
import random
import sys
import logging
from typing import Dict, Any, List, Tuple
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


# ??? It looks weird
def perform_random_walk(G: Graph, starting_node, left_side, right_side) -> str:
    while True:
        neighbors = G.neighbors(starting_node)
        random_id = random.randint(0, len(neighbors) - 1)

        starting_node = neighbors[random_id]

        if starting_node in left_side:
            return "left"

        if starting_node in right_side:
            return "right"


def perform_random_walk_full(G, starting_node, user_nodes) -> int:
    seen_nodes = {}  # contains unique nodes seen till now

    step_count = 0

    while step_count < (len(G.edges()) ** 2):
        step_count += 1

        neighbors = G.neighbors(starting_node)
        random_id = random.randint(0, len(neighbors) - 1)

        starting_node = neighbors[random_id]

        if starting_node in user_nodes:
            seen_nodes[starting_node] = 1

            if len(seen_nodes) == len(user_nodes):
                break

        if step_count % 100_000 == 0:
            print(f"{step_count} steps reached", file=sys.stderr)

    return step_count


def get_left_right_communities(communities_file: str) -> List[List[str], List[str]]:
    out = []

    # 1: left, and 2:right
    for i in [1, 2]:
        f = open(
            f"../communities_retweet_networks/community{i}_{communities_file}.txt")

        l = [line.strip() for line in f.readlines()]

        out.append(l)

    return out


def RWC(G, X, Y) -> float:
    k_left = int(precent * len(X))
    k_right = int(precent * len(Y))

    # start_end
    left_left = 0  # start at left ended at left
    left_right = 0
    right_left = 0
    right_right = 0

    for j in range(1, 1000):
        left_user_nodes = get_random_nodes_from_labels(
            X, Y, k=k_left, flag=LabelType.LEFT)  # TODO : return a list of nodes
        right_user_nodes = get_random_nodes_from_labels(
            X, Y, k=k_right, flag=LabelType.RIGHT)
        # Left community:

        K = None  # ! FIXME
        for i in range(K):
            crnt_node = left_user_nodes[i]

            other_nodes = left_user_nodes.copy()
            other_nodes.pop(i)

            side = perform_random_walk(
                G, crnt_node, left_user_nodes, right_user_nodes)  # ! FIXME avoid extra data

            if side == "left":  # ! FIXME: change to enum
                left_left += 1
            else:
                left_right += 1

        # Right community
        K = None  # ! FIXME
        for i in range(K):
            crnt_node = right_user_nodes[i]

            other_nodes = right_user_nodes.copy()
            other_nodes.pop(i)

            side = perform_random_walk(
                G, crnt_node, left_user_nodes, right_user_nodes)  # ! FIXME avoid extra data

            if side == "left":  # ! FIXME: change to enum
                right_left += 1
            else:
                right_right += 1

    e1 = left_left * 1.0 / (left_left + right_left)
    e2 = left_right * 1.0 / (left_right + right_right)
    e3 = right_left * 1.0 / (left_left + right_left)
    e4 = right_right * 1.0 / (left_right + right_right)

    score = e1*e4 - e2*e3

    return score


if __name__ == "__main__":

    # for testing and debuging. It's used if the user doesn't provide his arguments
    graph_file = "political_blogs_largest_CC.txt"
    communities_file = ""
    precent = 0

    if len(sys.argv) == 4:
        graph_file = sys.argv[1]
        communities_file = sys.argv[2]
        percent = float(sys.argv[3])/100

    # Read the graph
    G = nx.read_weighted_edgelist(graph_file, delimiter=',')

    # Get the left and right communities
    [left, right] = get_left_right_communities(communities_file)

    score = RWC(G, left, right)
