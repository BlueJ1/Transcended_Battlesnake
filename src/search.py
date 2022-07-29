from typing import List
import itertools
from time import time

from avoid import avoid_obstacles
from utils import deep_copy, get_snake  # , head_body_distance

MOVE_DIRECTION = {"up": (0, 1), "down": (0, -1), "right": (1, 0), "left": (-1, 0)}
TIME_LIMIT = 0.42
DEPTH_LIMIT = 5
# CONSIDERED_DISTANCE = int(1. * DEPTH_LIMIT)


def remove_certain_deaths(state: dict, possible_moves: List[str], t: float, time_limit: float = TIME_LIMIT) \
        -> List[str]:

    if len(possible_moves) <= 1:
        return possible_moves

    my_id = state["you"]["id"]
    # print(f'possible moves: {possible_moves}')
    new_states_per_move = {move: simulate_turn(move, my_id, state) for move in possible_moves}

    removed = []

    l = 1
    while True:
        certain_deaths = []
        for move in possible_moves:
            # print(f' selected move: {move}')
            # move_safe = True
            for new_state in new_states_per_move[move]:
                if not dls_survival(new_state, 1, l, t, time_limit):
                    certain_deaths.append(move)
                    # move_safe = False
                    break

            # print(f'Move {move} found to be {"safe" if move_safe else "deadly"}.')

        for move in certain_deaths:
            possible_moves.remove(move)
            removed.append((move, l))

        if time() - t > time_limit:
            print(f'reached depth: {l}')
            break

        l += 1

    # if all moves are discarded within the considered search depth, take the next-best one, as the opponents might not
    # play optimally
    highest_depth = 0
    best_alternative = ""
    if len(possible_moves) == 0:
        for i in range(len(removed)):
            if removed[i][1] > highest_depth:
                best_alternative = removed[i][0]
                highest_depth = removed[i][1]
        possible_moves = [best_alternative]

    return possible_moves


def dls_survival(state: dict, d: int, l: int, t: float, time_limit: float):
    """
    Simple recursive depth-limited search for sequences of moves that ensure survival.
    """

    if time() - t > time_limit:
        return 1

    my_id = state["you"]["id"]

    possible_moves = ["up", "down", "left", "right"]
    possible_moves = avoid_obstacles(state["you"]["head"], state, possible_moves)
    # print(possible_moves)

    if len(possible_moves) == 0:
        # print("Found deadly branch1")
        return 0
    elif d >= l:
        return 1  # success if we reach the depth limit and still have moves left

    for move in possible_moves:
        move_ensures_survival = True
        # print(f'd={d}, move={move}')
        for new_state in simulate_turn(move, my_id, state):
            if not dls_survival(new_state, d + 1, l, t, time_limit):
                # print(f'd={d}, move={move}, move_ensures_survival={move_ensures_survival}')
                move_ensures_survival = False
                break
        if move_ensures_survival:
            # print(f'd={d}, move={move}, move_ensures_survival={move_ensures_survival}')
            return 1

    # print("Found deadly branch2")
    return 0


def simulate_turn(my_move: str, my_id: str, state: dict) -> List[dict]:
    new_state = deep_copy(state)
    my_snake = get_snake(my_id, new_state["board"]["snakes"])
    new_state = simulate_move(my_move, my_snake, new_state)

    considered_snakes = []
    for snake in new_state["board"]["snakes"]:
        if snake["id"] != new_state["you"]["id"]:  # and head_body_distance(my_snake, snake) < CONSIDERED_DISTANCE:
            considered_snakes.append(snake)

    moves_considered_snakes = [[(move, snake) for move in avoid_obstacles(snake["head"], new_state,
                                                                          ["up", "down", "left", "right"])]
                               for snake in considered_snakes]

    possible_outcomes = []

    for moves in itertools.product(*moves_considered_snakes):
        new_state2 = deep_copy(new_state)
        for move, snake in moves:
            new_state2 = simulate_move(move, snake, new_state2)

        # check head collisions
        dead_snakes = []
        for snake in new_state2["board"]["snakes"]:
            for other_snake in new_state2["board"]["snakes"]:
                if snake["id"] != other_snake["id"] and snake["head"] == other_snake["head"]:
                    if snake["health"] < other_snake["health"]:
                        dead_snakes.append(snake)
                    elif snake["health"] > other_snake["health"]:
                        dead_snakes.append(other_snake)
                    else:
                        dead_snakes.append(snake)
                        dead_snakes.append(other_snake)

        i = 0
        while i < len(dead_snakes):
            if dead_snakes[i] in dead_snakes[i:]:
                dead_snakes.pop(i)
            else:
                i += 1

        for dead_snake in dead_snakes:
            new_state2["board"]["snakes"].remove(dead_snake)

        if alive(new_state2["board"]["snakes"], new_state2["you"]["id"]):
            possible_outcomes.append(new_state2)

    if len(possible_outcomes) == 0:
        possible_outcomes = [new_state]

    return possible_outcomes


def alive(snakes, snake_id):
    """
    Checks if the snake with ID == snake_id is still alive.
    """

    return any([snake_id == snake["id"] for snake in snakes])


def simulate_move(move: str, snake: dict, state: dict) -> dict:
    """
    state: current state of the game
    move: one out of [ up, down, left, right ]
    snake: the players snake

    return: the state of the game after the move
    TODO: misses a check for 0 health
    """
    head = snake["head"]

    # food consumption
    ate = False
    if head in state["board"]["food"]:
        state["board"]["food"].remove(head)
        ate = True

    # set new head position
    new_head = {"x": head["x"] + MOVE_DIRECTION[move][0],
                "y": head["y"] + MOVE_DIRECTION[move][1]}
    snake["body"] = [new_head] + (snake["body"] if ate else snake["body"][:-1])

    snake["head"] = new_head
    snake["health"] -= 1

    if new_head in state["board"]["food"]:
        snake["health"] = 100

    """"if snake["health"] == 0:
        state["board"]["snakes"].remove(snake)"""

    if snake["id"] == state["you"]["id"]:
        state["you"] = snake
        state["turn"] += 1

    # probably can be removed – reengineer to having snake_id as argument instead of snake
    #                         - can only be reengineered if [snakes] is transformed to dict {id: snake}
    for i in range(len(state["board"]["snakes"])):
        if state["board"]["snakes"][i]["id"] == snake["id"]:
            state["board"]["snakes"][i] = snake

    return state
