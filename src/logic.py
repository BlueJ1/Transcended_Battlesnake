import random
from typing import List, Dict
from utils import *

"""
This file can be a nice home for your Battlesnake's logic and helper functions.

We have started this for you, and included some logic to remove your Battlesnake's 'neck'
from the list of possible moves!
"""


def get_info() -> dict:
    """
    This controls your Battlesnake appearance and author permissions.
    For customization options, see https://docs.battlesnake.com/references/personalization

    TIP: If you open your Battlesnake URL in browser you should see this data.
    """

    return {
        "apiversion": "1",
        "author": "BlueJ1",
        "color": "#783F04",
        "head": "sand-worm",
        "tail": "round-bum",
    }


def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """

    my_snake = data["you"]      # A dictionary describing your snake's position on the board
    my_head = my_snake["head"]  # A dictionary of coordinates like {"x": 0, "y": 0}
    # A list of coordinate dictionaries like [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    my_body = my_snake["body"]

    board = data['board']
    board_height, board_width = board['height'], board['width']
    other_snakes = board["snakes"]

    # Uncomment the lines below to see what this data looks like in your output!
    # print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    # print(f"All board data this turn: {data}")
    # print(f"My Battlesnake this turn is: {my_snake}")
    # print(f"My Battlesnakes head this turn is: {my_head}")
    # print(f"My Battlesnakes body this turn is: {my_body}")

    possible_moves = ["up", "down", "left", "right"]

    # Step 0: Don't allow your Battlesnake to move back on it's own neck.
    possible_moves = _avoid_my_neck(my_body, possible_moves)

    # TODO: Step 1 - Don't hit walls.
    # Use information from `data` and `my_head` to not move beyond the game board.
    possible_moves = _avoid_wall(my_body, possible_moves, board_height=board_height, board_width=board_width)

    # TODO: Step 2 - Don't hit yourself.
    possible_moves = _avoid_body(my_body, possible_moves)
    # Use information from `my_body` to avoid moves that would collide with yourself.

    # TODO: Step 3 - Don't collide with others.
    # Use information from `data` to prevent your Battlesnake from colliding with others.
    possible_moves = _avoid_other_snakes(my_head, other_snakes, possible_moves)

    # TODO: Step 4 - Find food.
    # Use information in `data` to seek out and find food.
    food = data['board']['food']
    if len(food) > 0:
        closest_food = find_closest(my_head, food)
        move = _move_towards(my_head, closest_food, possible_moves)
    else:
        move = _pseudo_random(my_head, board_height, board_width, possible_moves)

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    # move = random.choice(possible_moves)
    # TODO: Explore new strategies for picking a move that are better than random

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move


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


def _avoid_wall(body: List[dict], possible_moves: List[str], board_height: int, board_width: int) -> List[str]:
    """
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with directions
            which would lead the snake outside the boundaries removed.
    """

    if len(possible_moves) <= 1:
        return possible_moves

    head = body[0]
    print(f'head_x: {head["x"]}, head_y: {head["y"]}')

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

    if len(possible_moves) <= 1:
        return possible_moves

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

    if len(possible_moves) <= 1:
        return possible_moves

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


def _move_towards(head: dict, goal: dict, possible_moves: List[str]) -> str:

    hx, hy = head["x"], head["y"]
    gx, gy = goal["x"], goal["y"]
    dx, dy = abs(hx - gx), abs(hy - gy)

    if dx >= dy and hx < gx and "right" in possible_moves:
        return "right"
    elif dx >= dy and hx > gx and "left" in possible_moves:
        return "left"
    elif dx < dy and hy < gy and "up" in possible_moves:
        return "up"
    elif dx < dy and hy > gy and "down" in possible_moves:
        return "down"
    else:  # reached automatically if head == goal
        return random.choice(possible_moves)


def _pseudo_random(head: dict, height: int, width: int, possible_moves: List[str]) -> str:
    hx, hy = head["x"], head["y"]
    if hx == 0 and "right" in possible_moves:
        return "right"
    elif hx + 1 == width and "left" in possible_moves:
        return "left"
    elif hy == 0 and "up" in possible_moves:
        return "up"
    elif hy + 1 == height and "down" in possible_moves:
        return "down"
    else:
        return random.choice(possible_moves)
