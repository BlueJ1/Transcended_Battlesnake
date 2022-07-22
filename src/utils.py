import os
from typing import List

import pandas as pd


def log(move: str, data: dict = None, log_file: str = None):
    if log_file is None:
        log_file = "move_log.csv"

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
