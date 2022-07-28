from typing import List


def avoid_obstacles(my_head: dict, state: dict, possible_moves: List[str]) -> List[str]:
    """
    Universal function to eliminate all moves that are against the rules, bundling more specific functions.

    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    other_snakes: List of dictionaries with information about the other Battlesnakes in the game.
            Keywords for every item: 'id', 'name', 'latency', 'health', 'body', 'head', 'length', 'shout', 'squad' and
            'customizations'
            Each item contains a list of dictionaries with x/y coordinates of the corresponding body (key 'body'):
            e.g. [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    hazards: List of dictionaries with information about the location of hazards in the game.
            e.g. [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    board_height: Int indicating height of the game board.
    board_width: Int indicating width of the game board.
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with directions which would be against the rules removed.
            This list CAN BE EMPTY.
    """

    board = state["board"]
    ruleset = state["ruleset"]["name"]

    if not ruleset == "wrapped":
        possible_moves = _avoid_wall(my_head, board["height"], board["width"], possible_moves)
    possible_moves = _avoid_snake_bodies(my_head, board["snakes"], possible_moves)
    possible_moves = _avoid_hazards(my_head, board["hazards"], possible_moves)

    return possible_moves


def _avoid_wall(head: dict, board_height: int, board_width: int, possible_moves: List[str]) -> List[str]:
    """
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    board_height: Int indicating height of the game board.
    board_width: Int indicating width of the game board.
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with directions
            which would lead the snake outside the boundaries removed.
    """

    if "right" in possible_moves and (head['x'] + 1) == board_width:
        possible_moves.remove("right")
    if "left" in possible_moves and (head['x'] - 1) < 0:
        possible_moves.remove("left")
    if "up" in possible_moves and (head['y'] + 1) == board_height:
        possible_moves.remove("up")
    if "down" in possible_moves and (head['y'] - 1) < 0:
        possible_moves.remove("down")

    return possible_moves


def _avoid_snake_bodies(my_head: dict, snakes: List[dict], possible_moves: List[str]):
    """
    head: Dictionary with x/y coordinates of the Battlesnake's head.
            e.g. {"x": 0, "y": 0}
    snakes: List of dictionaries with information about all Battlesnakes in the game.
            Keywords for every item: 'id', 'name', 'latency', 'health', 'body', 'head', 'length', 'shout', 'squad' and
            'customizations'
            Each item contains a list of dictionaries with x/y coordinates of the corresponding body (key 'body'):
            e.g. [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves,
            with directions which would lead the head into a body part of a snake.
    """

    # can this be made more efficient?

    hx, hy = my_head.values()

    for snake in snakes:
        for snake_part in snake["body"]:
            x, y = snake_part.values()
            if "right" in possible_moves and hx + 1 == x and hy == y:
                possible_moves.remove("right")
            if "left" in possible_moves and hx - 1 == x and hy == y:
                possible_moves.remove("left")
            if "up" in possible_moves and hx == x and hy + 1 == y:
                possible_moves.remove("up")
            if "down" in possible_moves and hx == x and hy - 1 == y:
                possible_moves.remove("down")

    return possible_moves


def _avoid_hazards(head: dict, hazards: List[dict], possible_moves: List[str]) -> List[str]:
    """
    head: Dictionary with x/y coordinates of the Battlesnake's head.
            e.g. {"x": 0, "y": 0}
    hazards: List of dictionaries with information about the location of hazards in the game.
            e.g. [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves,
            with directions which would lead the snake into a hazard.
    """

    hx, hy = head.values()

    for hazard in hazards:
        x, y = hazard.values()
        if "right" in possible_moves and hx + 1 == x and hy == y:
            possible_moves.remove("right")
        if "left" in possible_moves and hx - 1 == x and hy == y:
            possible_moves.remove("left")
        if "up" in possible_moves and hx == x and hy + 1 == y:
            possible_moves.remove("up")
        if "down" in possible_moves and hx == x and hy - 1 == y:
            possible_moves.remove("down")

    return possible_moves
