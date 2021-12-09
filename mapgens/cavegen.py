from __future__ import annotations
import random, inspect
from typing import Iterator, List, Tuple, TYPE_CHECKING

import numpy as np

import tcod
import entity_factories
from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


def generate_dungeon(
    map_width: int,
    map_height: int,
    engine: Engine,
    player: Entity,
) -> GameMap:
    """Generate a new cave map."""

    #mapcells = np.full((map_width, map_height), True, dtype=bool)
    
    wall_chance = .45
    mapcells = np.random.choice(a=[True, False], size=(map_width, map_height), p=[wall_chance, 1-wall_chance])  
    for x in range(5):
        mapcells = smooth_walls(mapcells)
 

    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])
    player.place(*(1,1), dungeon)

    dungeon.tiles[mapcells] = tile_types.wall
    return dungeon

def smooth_walls(cells):
    max_neighbors = 3
    min_neighbors = 2
    rebirth_neighbors = 3
    new_cells = np.full(cells.shape, True, dtype=bool)
    max_x = cells.shape[0]
    max_y = cells.shape[1]
   
    for ix, iy in np.ndindex(cells.shape):
        count = 0
        for x in range(-1,2):
            for y in range(-1,2):
                if not (x == 0 and y == 0):
                    if x+ix >= max_x or y+iy >= max_y or x+ix < 0 or y+iy < 0:
                        count += 1
                    elif(cells[ix+x,iy+y]):
                        count += 1
        if cells[ix,iy]:
            if count < min_neighbors:
                new_cells[ix,iy] = False
            elif count > max_neighbors:
                new_cells[ix,iy] = False
            else:
                new_cells[ix,iy] = cells[ix,iy]
        elif not cells[ix,iy] and count == 3:
            new_cells[ix,iy] = True
        else:
            new_cells[ix,iy] = cells[ix,iy]
    return new_cells
    