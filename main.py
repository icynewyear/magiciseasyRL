#!/usr/bin/env python3

import copy
import tcod

import color
import entity_factories
from engine import Engine
from game_map import GameMap
from input_handlers import EventHandler
#from procgen import generate_dungeon
from mapgens.cavegen import generate_dungeon

def main() -> None:
    ASSET_ROOT = "assets"
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    max_monsters_per_room = 0

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.game_map = generate_dungeon(
        #max_rooms=max_rooms,
        #room_min_size=room_min_size,
        #room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        #max_monsters_per_room=max_monsters_per_room,
        player=player,
        engine=engine,
        num_runs=4,
        seed=12213123,
        enclose=False
    )
    tileset = tcod.tileset.load_tilesheet(
        ASSET_ROOT+"\dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    engine.update_fov()

    engine.message_log.add_message(
        "Magic is easy.", color.welcome_text
    )
    engine.message_log.add_message(
        "Howl at a god.", color.welcome_text
    )
    with tcod.context.new_terminal(
        screen_width+40,
        screen_height,
        tileset=tileset,
        title="Magic is Easy",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width+40, screen_height, order="F")
        while True:

            engine.render(console=root_console, context=context)
            engine.event_handler.handle_events()



if __name__ == "__main__":
    main()
