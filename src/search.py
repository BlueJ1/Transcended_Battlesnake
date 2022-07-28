from typing import List
import itertools

from avoid import avoid_obstacles
from utils import deep_copy


def dls_survival(state: dict, d: int, l: int):
    """
    Simple recursive depth-limited search for sequences of moves that ensure survival.
    """

    my_head = state["you"]["head"]
    my_id = state["you"]["id"]
    board = state["board"]
    # TODO consider more relevant data (e.g. health)

    if d == l:
        return 1  # success if we reach the depth limit

    possible_moves = ["up", "down", "left", "right"]
    possible_moves = avoid_obstacles(my_head, board, possible_moves)

    if len(possible_moves) == 0:
        return 0

    for move in possible_moves:
        for new_state in simulate_turn(move, my_id, state):
            if dls_survival(new_state, d + 1, l):
                return 1

    return 0


def simulate_turn(my_move: str, my_id, state: dict) -> List[dict]:
    state = deep_copy(state)
    state = simulate_move(my_move, my_id, state)

    other_snakes = [snake if snake["id"] != state["you"]["id"] else None for snake in state["board"]["snakes"]]
    other_snakes.remove(None)
    moves_other_snakes = [[(move, snake["id"]) for move in avoid_obstacles(snake["head"], state["board"],
                                                                           ["up", "down", "left", "right"])]
                          for snake in other_snakes]

    possible_outcomes = []
    for moves in itertools.product(*moves_other_snakes):
        new_state = deep_copy(state)
        for move, snake_id in moves:
            new_state = simulate_move(move, snake_id, state)

        if alive(new_state["board"]["snakes"], new_state["you"]["id"]):
            possible_outcomes.append(new_state)

    return possible_outcomes


def alive(snakes, snake_id):
    """
    Checks if the snake with ID == snake_id is still alive.
    """

    return any([snake_id == snake["id"] for snake in snakes])


def simulate_move(move: str, snake_id: str, state: dict) -> dict:
    pass
