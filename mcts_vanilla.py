
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

    def utc_sort(child):
        return child.wins / child.visits + sqrt(2*log(node.visits) / child.visits)

    def select_most_urgent(node):
        return sorted(node.child_nodes, utc_sort)[-1]

    #find the node that has child and no unexplored actions
    while node.untried_actions == [] and len(node.child_nodes) != 0:
        #use UTC to find the most urgent node
        node = select_most_urgent(node)
        state = board.next_state(node.parent_action)

    if node.untried_actions != []:
        #select an unexpanded node at random
        r_action = choice(node.untried_actions)
        node.untried_actions.remove(r_action)
        #expand it
        return expand_leaf(node, board, board.next_state(r_action))

    return None

def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """
    if node.untried_actions != []:
        action = choice(node.untried_actions)
        node.untried_actions.remove(action)
        next_state = board.next_state(state, action)
        new_node = MCTSNode(parent=node, parent_action=action, action_list=board.legal_actions(next_state))
        node.child_nodes[action] = new_node
        new_node.wins = rollout(board, next_state)
        return new_node
    return None
    # Hint: return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    
    for action in board.legal_actions(state):
        next_state = board.next_state(action)

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
        leaf = traverse_nodes(node, board, sampled_game, identity_of_bot)
        rollout(board, board.next_state(choice(leaf.untried_actions)))

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return None
