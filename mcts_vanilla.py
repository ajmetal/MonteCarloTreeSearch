
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log, inf
from heapq import heappop, heappush
from random import random, randint

num_nodes = 100
explore_faction = 2.

def heuristic(node):
    return random()

def get_leaves(node, leaf_nodes):
    for child in node.child_nodes:
        for action in child.untried_actions:
            if child.child_nodes[action] != None:
                heappush(leaf_nodes, (heuristic(child), child))
                break

def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    leaf_nodes = []

    get_leaves(node, leaf_nodes)

    val, leaf = heappop(leaf_nodes)

    return leaf

def calculate_state(node, board, state):
    if node.parent == None:
        return state
    else
        new_state = calculate_state(node.parent, board, state)
        return board.next_state(new_state, node.parent_action)

def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """
    #root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))
    state = calculate_state(node, board, state)

    new_action = None
    for action in node.untried_actions:
        if node.child_nodes[action] == None:
            new_action = action
            break

    new_state = board.next_state(board, new_action)
    new_node = MCTSNode(parent=node, parent_action=new_action, action_list=board.legal_actions(new_state))
    #node.child_nodes[action] = MCTSNode(parent=node, parent_action=new_action, action_list=board.legal_actions(new_state))

    new_node.wins = rollout(board, new_state)
    node.child_nodes[action] = new_node
    backpropagate(new_node, 0)

    return node
    # Hint: return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    while !board.is_ended(state):
        actions = board.legal_actions(state)
        action = actions[randint(0, len(actions) - 1)]
        state = board.next_state(state, action)

    return board.points_value(state)



def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    if node.parent != None:
        backpropagate(node.parent, won + node.wins)


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        leaf = traverse_nodes(node, board, sampled_game, identity_of_bot)
        expand_leaf(leaf, board, sampled_game)

    max_val = -inf
    max_node = None
    for child in root_node.child_nodes:
        if child.wins / child.visits > max_val:
            max_node = child
            max_val = child.wins/child.visits

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return max_node.parent_action
