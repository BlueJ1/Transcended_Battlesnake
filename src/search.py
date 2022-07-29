from typing import List
import itertools
# from time import time

from avoid import avoid_obstacles
from utils import deep_copy, head_body_distance, get_snake

move_direction = {"up": (0, 1), "down": (0, -1), "right": (1, 0), "left": (-1, 0)}
DEPTH_LIMIT = 5
CONSIDERED_DISTANCE = int(1.5 * DEPTH_LIMIT)


def remove_certain_deaths(state: dict, possible_moves: List[str], l: int = DEPTH_LIMIT) -> List[str]:
    # t = time()
    my_id = state["you"]["id"]
    for move in possible_moves:
        move_possible = True
        for new_state in simulate_turn(move, my_id, state):
            if not dls_survival(new_state, 1, l):
                move_possible = False
                break

        if not move_possible:
            print("Removed " + move + " in remove_certain_deaths.")
            possible_moves.remove(move)

    # print("time:", time() - t)

    return possible_moves


def dls_survival(state: dict, d: int, l: int):
    """
    Simple recursive depth-limited search for sequences of moves that ensure survival.
    """

    my_id = state["you"]["id"]
    # TODO consider more relevant data (e.g. health)

    possible_moves = ["up", "down", "left", "right"]
    possible_moves = avoid_obstacles(state["you"]["head"], state, possible_moves)

    if len(possible_moves) == 0:
        print("Found deadly branch")
        return 0
    elif d >= l:
        return 1  # success if we reach the depth limit and still have moves left

    for move in possible_moves:
        move_ensures_survival = True
        for new_state in simulate_turn(move, my_id, state):
            if not dls_survival(new_state, d + 1, l):
                move_ensures_survival = False
                break
        if move_ensures_survival:
            return 1

    print("Found deadly branch")
    return 0


def simulate_turn(my_move: str, my_id: str, state: dict) -> List[dict]:
    my_snake = get_snake(my_id, state["board"]["snakes"])
    state = deep_copy(state)
    simulate_move(my_move, my_snake, state)

    considered_snakes = []
    for snake in state["board"]["snakes"]:
        if snake["id"] != state["you"]["id"] and head_body_distance(my_snake, snake) < CONSIDERED_DISTANCE:
            considered_snakes.append(snake)

    moves_considered_snakes = [[(move, snake) for move in avoid_obstacles(snake["head"], state,
                                                                          ["up", "down", "left", "right"])]
                               for snake in considered_snakes]

    possible_outcomes = []

    for moves in itertools.product(*moves_considered_snakes):
        new_state = deep_copy(state)
        for move, snake in moves:
            simulate_move(move, snake, state)

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


def simulate_move(move: str, snake: dict, state: dict):
    head = snake["head"]
    new_head = {"x": head["x"] + move_direction[move][0], "y": head["y"] + move_direction[move][1]}
    snake["body"] = [new_head] + snake["body"][:-1]

    snake["head"] = new_head
    snake["health"] -= 1

    if new_head in state["board"]["food"]:
        snake["health"] = 100
        state["board"]["food"].remove(new_head)

    if snake["health"] == 0:
        state["board"]["snakes"].remove(snake)

    if snake["id"] == state["you"]["id"]:
        state["you"] = snake
        state["turn"] += 1
