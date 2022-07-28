import os
from typing import List

import pandas as pd


def log(move: str, data: dict = None, log_file: str = None):
    if log_file is None:
        log_file = "move_log.csv"

    log_file = "../logs/" + log_file

    if os.path.isfile(log_file):
        os.mkdir(log_file)

    move_history = pd.read_csv(log_file)
    move_history.loc[len(move_history.index)] = [move]
    move_history.to_csv(log_file)


def read_logs(log_file: str = None) -> List[str]:
    if log_file is None:
        log_file = "move_log.csv"

    move_history = pd.read_csv(log_file)
    move_history = move_history.values.tolist()

    return move_history


def find_closest(p: dict, qs: List[dict], metric: str = "Manhattan"):
    """
    p: Dictionary with x/y coordinates of a point p
            e.g. {"x": 0, "y": 0}
    qs: List of dictionaries with x/y coordinates of points, of which one has to be chosen as closest to p
            e.g. [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    metric: Str indicating the method by which closeness is determined
            e.g. "Manhattan"

    return: The dictionary with x/y coordinates of a point in qs that is closest to p by the specified metric
    """

    if len(qs) == 1:
        return qs[0]
    elif len(qs) == 0:
        return p

    if metric == "Manhattan":
        px, py = p["x"], p["y"]
        best_distance = abs(px - qs[0]["x"]) + abs(py - qs[0]["y"])
        best_q = qs[0]
        for q in qs[1:]:
            distance = abs(px - q["x"]) + abs(py - q["y"])
            if distance < best_distance:
                best_distance = distance
                best_q = q
    else:
        raise ValueError(f'Distance metric {metric} not implemented.')

    return best_q


def deep_copy(obj):
    if type(obj) == list:
        new_obj = []
        for item in obj:
            new_obj.append(deep_copy(item))
    elif type(obj) == dict:
        new_obj = {}
        for key, val in obj.items():
            new_obj[key] = deep_copy(val)  # assuming only strings as keys
    elif type(obj) == str or type(obj) == int:
        new_obj = obj
    else:
        raise ValueError(f'Cannot copy object {obj}')

    return new_obj
