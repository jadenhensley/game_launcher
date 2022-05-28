import os, sys, subprocess
import shutil
import path_util

PROJECT_PATH = path_util.get_project_directory()

game_data = {
    "games":{
        "snake":{
            "repository":"https://github.com/jadenhensley/snake",
            "title":"Snake",
            "icon":"games/snake/icon.png",
            "executable":"games/snake/snake.py"
        }
    }
}