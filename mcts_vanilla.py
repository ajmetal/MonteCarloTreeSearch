
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log, inf
import random
from timeit import default_timer as time

num_nodes = 1000
explore_fraction = 2.

def heuristic(node, depth):
    winrate = node.wins/node.visits
    if node.parent == None:
        explore = 100
    else:
        # = .29 + 2 * sqrt(2*log(801)/7)
        explore = explore_fraction * sqrt(2*log(node.parent.visits) / node.visits)
        #explore = explore_fraction * (node.parent.visits / node.visits)
    return winrate + explore
    #return random()

def get_leaves(node, leaf_nodes, depth):
    if(len(node.untried_actions) > 0):
        leaf_nodes.insert(0, (heuristic(node, depth), node))

    if(len(leaf_nodes) > 0):
        return
    else:
        best_heur = -1
        best_node = None
        for child in node.child_nodes:
            heur = heuristic(node.child_nodes[child], depth + 1)
            if heur > best_heur:
                best_heur = heur
                best_node = node.child_nodes[child]
        if best_node != None:
            get_leaves(best_node, leaf_nodes, depth + 1)

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

    best_node = get_leaves(node, leaf_nodes, 0)

    max_val = -1
    for i in range(0, len(leaf_nodes)):
        if leaf_nodes[i][0] > max_val:
            best_node = leaf_nodes[i][1]
            max_val = leaf_nodes[i][0]

    return best_node

def calculate_state(node, board, state):
    if node.parent == None:
        return state
    else:
        new_state = calculate_state(node.parent, board, state)
        return board.next_state(new_state, node.parent_action)

def expand_leaf(node, board, state, identity):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """
    #root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))
    state = calculate_state(node, board, state)

    new_action = node.untried_actions[0]
    node.untried_actions.remove(new_action)

    new_state = board.next_state(state, new_action)
    new_node = MCTSNode(parent=node, parent_action=new_action, action_list=board.legal_actions(new_state))

    new_node.wins = rollout(board, new_state)[identity]
    new_node.visits = 1
    node.child_nodes[new_action] = new_node
    backpropagate(node, new_node.wins)

    return node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    while not board.is_ended(state):
        actions = board.legal_actions(state)
        action = random.choice(actions)
        state = board.next_state(state, action)

    return board.points_values(state)



def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    node.visits += 1
    node.wins += won
    if node.parent != None:
        backpropagate(node.parent, won)


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))
    root_node.visits = 1

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        leaf = traverse_nodes(node, board, sampled_game, identity_of_bot)
        if leaf != None:
            expand_leaf(leaf, board, sampled_game, identity_of_bot)
        else:
            break

    max_val = -inf
    max_node = None
    
    for child in root_node.child_nodes:
        if root_node.child_nodes[child].wins / root_node.child_nodes[child].visits > max_val:
            max_node = child
            max_val = root_node.child_nodes[child].wins / root_node.child_nodes[child].visits

    #print("VANILLA\ntime elapsed: ", time_elapsed, "\nroot visits: ", root_node.visits, "\n")
    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return root_node.child_nodes[max_node].parent_action
