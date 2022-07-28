import random
from typing import List
from utils import find_closest
from avoid import avoid_obstacles
from search import remove_certain_deaths

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


def choose_move(state: dict) -> str:
    """
    state: Dictionary of all Game Board data as received from the Battlesnake Engine, describing the current state of
            the game.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """

    my_snake = state["you"]      # A dictionary describing your snake's position on the board
    my_head = my_snake["head"]  # A dictionary of coordinates like {"x": 0, "y": 0}
    # A list of coordinate dictionaries like [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    my_body = my_snake["body"]

    board = state['board']
    board_height, board_width = board['height'], board['width']
    other_snakes = board["snakes"]
    hazards = board["hazards"]

    # Uncomment the lines below to see what this data looks like in your output!
    # print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    # print(f"All board data this turn: {data}")
    # print(f"My Battlesnake this turn is: {my_snake}")
    # print(f"My Battlesnakes head this turn is: {my_head}")
    # print(f"My Battlesnakes body this turn is: {my_body}")

    possible_moves = ["up", "down", "left", "right"]
    # Step 0 to 3 – eliminate impossible moves
    # TODO: merge the next two lines
    possible_moves = avoid_obstacles(my_head, state, possible_moves)
    possible_moves = remove_certain_deaths(state, possible_moves)

    if len(possible_moves) == 0:
        move = "up"  # the move returned here is irrelevant, as none is correct
        print("Found no valid move and therefore executing 'up'.")
    elif len(possible_moves) == 1:
        move = possible_moves[0]  # only option
    else:
        # Step 4 - Find food.
        # Use information in `data` to seek out and find food.
        food = board['food']
        if len(food) > 0:
            closest_food = find_closest(my_head, food)
            move = _move_towards(my_head, closest_food, board_height, board_width, possible_moves)
        else:
            # move = _pseudo_random(my_head, board_height, board_width, possible_moves)
            move = random.choice(possible_moves)

        # Choose a random direction from the remaining possible_moves to move in, and then return that move
        # move = random.choice(possible_moves)
        # TODO: Explore new strategies for picking a move that are better than random

    print(f"{state['game']['id']} MOVE {state['turn']}: {move} picked from all valid options in {possible_moves}")

    return move


def _move_towards(head: dict, goal: dict, board_height: int, board_width: int, possible_moves: List[str]) -> str:
    """
    head: Dictionary with x/y coordinates of the Battlesnake's head.
            e.g. {"x": 0, "y": 0}
    goal: Dictionary with x/y coordinates of the goal point.
            e.g. {"x": 0, "y": 0}
    board_height: Int indicating height of the game board.
    board_width: Int indicating width of the game board.
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: str;
            A chosen move, bringing the snake towards the goal point, prioritizing the axis with higher distance.
            If no move leads towards the goal, chooses a (pseudo) random one.
    """

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
        return _pseudo_random(head, board_height, board_width, possible_moves)


def _pseudo_random(head: dict, board_height: int, board_width: int, possible_moves: List[str]) -> str:
    """
    head: Dictionary with x/y coordinates of the Battlesnake's head.
            e.g. {"x": 0, "y": 0}
    board_height: Int indicating height of the game board.
    board_width: Int indicating width of the game board.
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: str;
            A chosen move that, if possible, brings the snake away from a wall, and otherwise is a random selection
            from possible_moves.
    """

    hx, hy = head["x"], head["y"]

    if hx == 0 and "right" in possible_moves:
        return "right"
    elif hx + 1 == board_width and "left" in possible_moves:
        return "left"
    elif hy == 0 and "up" in possible_moves:
        return "up"
    elif hy + 1 == board_height and "down" in possible_moves:
        return "down"
    else:
        return random.choice(possible_moves)
