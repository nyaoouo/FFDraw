import os

game_version = tuple(map(int, os.environ.get('FFXIV_GAME_VERSION').split('.')))
