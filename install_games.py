import os, sys, subprocess
import shutil
from game_data import PROJECT_PATH, game_data

def install_games():
    for game in game_data["games"]:
        href = game_data["games"][game]["repository"]

        if not os.path.isdir(f"{PROJECT_PATH}/{game}") and not os.path.isdir(f"{PROJECT_PATH}/games/{game}"):
            print(f"installing {game}...")
            git_clone = subprocess.run(f"git clone {href}", stdout=subprocess.PIPE, shell=True)
            message = git_clone.stdout.decode()
            print(message)
            print("moving to game directory...")
            shutil.move(f"{PROJECT_PATH}/{game}",f"{PROJECT_PATH}/games")
            print(f"installed {game}.\n\n")
        else:
            print(f"{game} is already installed.")

def install_game(game, repository):
    href = repository

    if not os.path.isdir(f"{PROJECT_PATH}/{game}") and not os.path.isdir(f"{PROJECT_PATH}/games/{game}"):
        print(f"installing {game}...")
        git_clone = subprocess.run(f"git clone {href}", stdout=subprocess.PIPE, shell=True)
        message = git_clone.stdout.decode()
        print(message)
        print("moving to game directory...")
        shutil.move(f"{PROJECT_PATH}/{game}",f"{PROJECT_PATH}/games")
        print(f"installed {game}.\n\n")
    else:
        print(f"{game} is already installed.")


if __name__ == "__main__":
    install_games()