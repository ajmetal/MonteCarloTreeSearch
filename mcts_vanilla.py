
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log, inf

num_nodes = 100
explore_faction = 2.

def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    min_child = None
    max_actions = 0
    for child in node.child_nodes:
        actions = len(child.untried_actions)
        if actions > 0 and actions > max_actions:
            min_child = child
            max_actions = actions

    #leaf = None
    if max_actions is 0:
        for child in node.child_nodes:
            nextState = board.next_state(state, child.parent_action)
            min_child = traverse_nodes(child, board, nextState, board.current_player(nextState))
            if min_child is not None:
                break

        """if child.visits is 0:
            return expand_leaf(child, board, board.next_state(state, child.parent_action))
        if child.visits < min_visits:
            min_visits = child.visits
            min_child = child"""
                
    #return leaf_node
    #board.next_state(state, min_child.parent_action)
    #return traverse_nodes(min_child, board, board.next_state(state, min_child.parent_action), identity)

    return min_child, board.next_state(min_child.parent_action)




def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """
    #root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))
    action = node.untried_actions[0]
    node.untried_actions.remove(action)
    next_state = board.next_state(state, action)
    new_node = MCTSNode(parent=node, parent_action=action, action_list=board.legal_actions(next_state))
    node.child_nodes[action] = new_node
    new_node.wins = rollout(board, next_state)
    return new_node
    # Hint: return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    return 0


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    pass


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
        leaf, new_state = traverse_nodes(node, board, sampled_game, identity_of_bot)
        new_leaf = expand_leaf(leaf, board, new_state)
        backpropagate(new_leaf)

    

    

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return None
