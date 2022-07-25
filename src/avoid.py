from typing import List


def avoid_obstacles(my_body: List[dict], other_snakes: List[dict], hazards: List[dict], board_height: int,
                    board_width: int, possible_moves: List[str]) -> List[str]:
    """
    Universal function to eliminate all moves that are against the rules.

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

    my_head = my_body[0]

    # Step 0: Don't allow your Battlesnake to move back on it's own neck.
    possible_moves = _avoid_my_neck(my_body, possible_moves)

    # Step 1 - Don't hit walls.
    # Use information from `data` and `my_head` to not move beyond the game board.
    possible_moves = _avoid_wall(my_body, board_height, board_width, possible_moves)

    # Step 2 - Don't hit yourself.
    # Use information from `my_body` to avoid moves that would collide with yourself.
    possible_moves = _avoid_body(my_body, possible_moves)

    # Step 3 - Don't collide with others.
    # Use information from `data` to prevent your Battlesnake from colliding with others.
    possible_moves = _avoid_other_snakes(my_head, other_snakes, possible_moves)

    # Step 4 – Don't hit obstacles.
    possible_moves = _avoid_hazards(my_head, hazards, possible_moves)

    return possible_moves


def _avoid_my_neck(my_body: List[dict], possible_moves: List[str]) -> List[str]:
    """
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    my_head = my_body[0]  # The first body coordinate is always the head
    my_neck = my_body[1]  # The segment of body right after the head is the 'neck'

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.remove("up")

    return possible_moves


def _avoid_wall(body: List[dict], board_height: int, board_width: int, possible_moves: List[str]) -> List[str]:
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

    head = body[0]

    if "right" in possible_moves and (head['x'] + 1) == board_width:
        possible_moves.remove("right")
    if "left" in possible_moves and (head['x'] - 1) < 0:
        possible_moves.remove("left")
    if "up" in possible_moves and (head['y'] + 1) == board_height:
        possible_moves.remove("up")
    if "down" in possible_moves and (head['y'] - 1) < 0:
        possible_moves.remove("down")

    return possible_moves


def _avoid_body(body: List[dict], possible_moves: List[str]) -> List[str]:
    """
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves,
            with directions which would lead the snake into its own body removed.
    """

    head = body[0]
    hx, hy = head.values()

    for body_part in body[1:]:
        x, y = body_part.values()
        if "right" in possible_moves and hx + 1 == x and hy == y:
            possible_moves.remove("right")
        if "left" in possible_moves and hx - 1 == x and hy == y:
            possible_moves.remove("left")
        if "up" in possible_moves and hx == x and hy + 1 == y:
            possible_moves.remove("up")
        if "down" in possible_moves and hx == x and hy - 1 == y:
            possible_moves.remove("down")

    return possible_moves


def _avoid_other_snakes(head: dict, other_snakes: List[dict], possible_moves: List[str]) -> List[str]:
    """
    head: Dictionary with x/y coordinates of the Battlesnake's head.
            e.g. {"x": 0, "y": 0}
    other_snakes: List of dictionaries with information about the other Battlesnakes in the game.
            Keywords for every item: 'id', 'name', 'latency', 'health', 'body', 'head', 'length', 'shout', 'squad' and
            'customizations'
            Each item contains a list of dictionaries with x/y coordinates of the corresponding body (key 'body'):
            e.g. [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves,
            with directions which would lead the snake into another snake.
    """

    hx, hy = head.values()

    for snake in other_snakes:
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
