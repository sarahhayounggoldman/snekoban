"""
6.1010 Spring '23 Lab 4: Snekoban Game
"""

import json
import typing

# NO ADDITIONAL IMPORTS!


direction_vector = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}


def new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, representing the
    locations of the objects on the board (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['wall'], ['computer']],
        [['target', 'player'], ['computer'], ['target']],
    ]

    The exact choice of representation is up to you; but note that what you
    return will be used as input to the other functions.
    """
    dct_representation = {
        "target": set(),
        "computer": set(),
        "wall": set(),
    }  


    for row_num, row in enumerate(level_description):
        for col_num, block in enumerate(row):
 
            if "player" in block:
                dct_representation["player"] = (row_num, col_num)

            if "target" in block:
                dct_representation["target"].add((row_num, col_num))

            if "computer" in block:
                dct_representation["computer"].add((row_num, col_num))

            if "wall" in block:
                dct_representation["wall"].add((row_num, col_num))

    dct_representation["row_num_stored"] = (
        row_num + 1
    )  # remember - careful of off by 1 errors
    dct_representation["col_num_stored"] = col_num + 1

    return dct_representation


def victory_check(game):
    """
    Given a game representation (of the form returned from new_game), return
    a Boolean: True if the given game satisfies the victory condition, and
    False otherwise.
    """

    if len(game["target"]) == 0:
        return False

    if len(game["target"]) > len(game["computer"]):
        return False

    for item in game["computer"]:
        if item not in game["target"]:
            return False

    return True


def step_game(game, direction):
    """
    Given a game representation (of the form returned from new_game), return a
    new game representation (of that same form), representing the updated game
    after running one step of the game.  The user's input is given by
    direction, which is one of the following: {'up', 'down', 'left', 'right'}.

    This function should not mutate its input.
    """
    new_player = (0, 0)
    new_computer_set = game["computer"].copy()

    player_r, player_c = game["player"]
    drow, dcol = direction_vector[direction]

    r, c = player_r + drow, player_c + dcol

    r2, c2 = r + drow, c + dcol

    if (r, c) in game["wall"]:
        return game

    if (r, c) in game["computer"]:
        if (r2, c2) in game["computer"]:
            return game
        if (r2, c2) in game["wall"]:
            return game

        new_player = (r, c)
        new_computer_set.remove((r, c))
        new_computer_set.add((r2, c2))

        return {
            "player": new_player,
            "target": game["target"],
            "computer": new_computer_set,
            "wall": game["wall"],
            "row_num_stored": game["row_num_stored"],
            "col_num_stored": game["col_num_stored"],
        }

    return {
        "player": (r, c),
        "target": game["target"],
        "computer": game["computer"],
        "wall": game["wall"],
        "row_num_stored": game["row_num_stored"],
        "col_num_stored": game["col_num_stored"],
    }


def dump_game(game):
    """
    Given a game representation (of the form returned from new_game), convert
    it back into a level description that would be a suitable input to new_game
    (a list of lists of lists of strings).

    This function is used by the GUI and the tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """
    game_to_return = []

    # build the skeleton
    for row in range(game["row_num_stored"]):
        game_to_return.append([])
        for col in range(game["col_num_stored"]):
            game_to_return[row].append([])

    for tup in game["computer"]:  # (1,0) for example
        row = tup[0]
        col = tup[1]
        game_to_return[row][col].append("computer")

    for tup in game["target"]:  # (1,0) for example
        row = tup[0]
        col = tup[1]
        game_to_return[row][col].append("target")

    player_tup = game["player"]
    game_to_return[player_tup[0]][player_tup[1]].append("player")

    for tup in game["wall"]:  # (1,0) for example
        row = tup[0]
        col = tup[1]
        game_to_return[row][col].append("wall")

    return game_to_return


def solve_puzzle(game):
    """
    Given a game representation (of the form returned from new game), find a
    solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None.
    """

    attempted_paths = set()
    candidate_paths = [
        ([], game),
    ]

    while candidate_paths:

        moves = ["left", "right", "up", "down"]
        path = candidate_paths.pop(0)

        if victory_check(path[1]) == True:
            return path[0]

        game_state = (path[1]["player"], frozenset(path[1]["computer"]))

        if game_state not in attempted_paths:
            attempted_paths.add(game_state)

            for move in moves:
                candidate_paths.append((path[0] + [move], step_game(path[1], move)))

    return None


if __name__ == "__main__":

    with open("test_levels/random_0000.json", "rb") as t0:
        pythonObj = json.load(t0)

    game = new_game(t0)

    # print(solve_puzzle(game))
