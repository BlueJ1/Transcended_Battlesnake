import os
from typing import List, Dict

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
    if len(qs) <= 1:
        return qs

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
