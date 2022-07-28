from typing import List
import itertools
from time import time

from avoid import avoid_obstacles
from utils import deep_copy, head_body_distance

direction_dxdy = {"up": (0, 1), "down": (0, -1), "right": (1, 0), "left": (-1, 0)}
CONSIDERED_DISTANCE = 12
DEPTH_LIMIT = 10


def remove_certain_deaths(state: dict, possible_moves: List[str], l: int = DEPTH_LIMIT) -> List[str]:
    t = time()
    my_snake = state["you"]
    for move in possible_moves:
        move_possible = False
        for new_state in simulate_turn(move, my_snake, state):
            if dls_survival(new_state, 1, l):
                move_possible = True
                break

        if not move_possible:
            possible_moves.remove(move)

    print("time:", time() - t)

    return possible_moves


def dls_survival(state: dict, d: int, l: int):
    """
    Simple recursive depth-limited search for sequences of moves that ensure survival.
    """

    if d >= l:
        return 1  # success if we reach the depth limit

    my_snake = state["you"]
    # TODO consider more relevant data (e.g. health)

    possible_moves = ["up", "down", "left", "right"]
    # possible_moves = avoid_obstacles(my_head, board, possible_moves)

    if len(possible_moves) == 0:
        return 0

    for move in possible_moves:
        for new_state in simulate_turn(move, my_snake, state):
            if dls_survival(new_state, d + 1, l):
                return 1

    return 0


def simulate_turn(my_move: str, my_snake, state: dict) -> List[dict]:
    state = deep_copy(state)
    state = simulate_move(my_move, my_snake, state)

    considered_snakes = []
    for snake in state["board"]["snakes"]:
        if snake["id"] != state["you"]["id"] and head_body_distance(my_snake, snake) < CONSIDERED_DISTANCE:
            considered_snakes.append(snake)

    moves_considered_snakes = [[(move, snake) for move in avoid_obstacles(snake["head"], state,
                                                                          ["up", "down", "left", "right"])]
                               for snake in considered_snakes]

    possible_outcomes = []

    print(f'Number of searched states = {len(list(itertools.product(*moves_considered_snakes)))}')

    for moves in itertools.product(*moves_considered_snakes):
        new_state = deep_copy(state)
        for move, snake in moves:
            new_state = simulate_move(move, snake, state)

        """
        # check head collisions
        for snake in new_state["board"]["snakes"]:
            for other_snake in new_state["board"]["snakes"]:
                if snake["id"] != other_snake["id"] and snake["head"] == other_snake["head"]:
                    if snake["health"] < other_snake["health"]:
                        new_state["board"]["snakes"].remove(snake)
                    elif snake["health"] > other_snake["health"]:
                        new_state["board"]["snakes"].remove(other_snake)
                    else:
                        new_state["board"]["snakes"].remove(snake)
                        new_state["board"]["snakes"].remove(other_snake)
        """

        if alive(new_state["board"]["snakes"], new_state["you"]["id"]):
            possible_outcomes.append(new_state)

    if len(possible_outcomes) == 0:
        possible_outcomes = [state]

    return possible_outcomes


def alive(snakes, snake_id):
    """
    Checks if the snake with ID == snake_id is still alive.
    """

    return any([snake_id == snake["id"] for snake in snakes])


def simulate_move(move: str, snake: dict, state: dict) -> dict:
    head = snake["head"]
    new_head = {"x": head["x"] + direction_dxdy[move][0], "y": head["y"] + direction_dxdy[move][1]}
    snake["body"] = [new_head] + snake["body"][:-1]

    snake["head"] = new_head
    """
    snake["health"] -= 1

    if new_head in state["board"]["food"]:
        snake["health"] = 100
        state["board"]["food"].remove(new_head)

    if snake["health"] == 0:
        state["board"]["snakes"].remove(snake)

    if snake["id"] == state["you"]["id"]:
        state["you"] = snake
        state["turn"] += 1
    """

    return state
