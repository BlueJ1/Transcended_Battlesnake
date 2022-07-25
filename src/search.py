from typing import List

from avoid import avoid_obstacles


def dls_survival(my_body: List[dict], board: dict, d: int, l: int):
    """
    Simple recursive depth-limited search for sequences of moves that ensure survival.
    """

    # TODO consider more relevant data (e.g. health)
    if d == l:
        return 1  # success if we reach the depth limit

    possible_moves = ["up", "down", "left", "right"]
    possible_moves = avoid_obstacles(my_body, board["other_snakes"], board["hazards"], board["height"], board["width"],
                                     possible_moves)

    if len(possible_moves) == 0:
        return 0

    for move in possible_moves:
        for new_body, new_board in simulate_turn(my_body, board, move):
            if dls_survival(new_body, new_board, d + 1, l):
                return 1

    return 0


def simulate_turn(body: List[dict], board: dict):
    pass
