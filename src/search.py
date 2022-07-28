from typing import List
import itertools

from avoid import avoid_obstacles
from utils import deep_copy


def remove_certain_deaths(state: dict, possible_moves: List[str], l: int = 1) -> List[str]:
    my_id = state["you"]["id"]
    for move in possible_moves:
        move_possible = False
        for new_state in simulate_turn(move, my_id, state):
            if dls_survival(new_state, 1, l):
                move_possible = True
                break

        if not move_possible:
            possible_moves.remove(move)

    return possible_moves


def dls_survival(state: dict, d: int, l: int):
    """
    Simple recursive depth-limited search for sequences of moves that ensure survival.
    """

    if d == l:
        return 1  # success if we reach the depth limit

    my_head = state["you"]["head"]
    my_id = state["you"]["id"]
    board = state["board"]
    # TODO consider more relevant data (e.g. health)

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

    return possible_outcomes


def alive(snakes, snake_id):
    """
    Checks if the snake with ID == snake_id is still alive.
    """

    return any([snake_id == snake["id"] for snake in snakes])


def simulate_move(move: str, snake_id: str, state: dict) -> dict:
    snake = {}
    for any_snake in state["board"]["snakes"]:
        if any_snake["id"] == snake_id:
            snake = any_snake
            break

    if "id" not in snake:
        print("Sought-after id:", snake_id)
        for any_snake in state["board"]["snakes"]:
            print(any_snake)
        raise ValueError(f'No snake with id == {snake_id}.')

    head = snake["head"]
    direction_dxdy = {"up": (0, 1), "down": (0, -1), "right": (1, 0), "left": (-1, 0)}
    new_head = {"x": head["x"] + direction_dxdy[move][0], "y": head["y"] + direction_dxdy[move][1]}
    new_body = [new_head] + snake["body"][:-1]

    snake["head"] = new_head
    snake["body"] = new_body
    snake["health"] -= 1

    if new_head in state["board"]["food"]:
        snake["health"] = 100
        state["board"]["food"].remove(new_head)

    if snake["health"] == 0:
        print("Ran out of health!!!!!!!!!!!!!!!!!!!")
        state["board"]["snakes"].remove(snake)

    if snake_id == state["you"]["id"]:
        state["you"] = snake
        state["turn"] += 1

    return state
