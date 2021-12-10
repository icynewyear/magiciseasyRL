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
    for x in range(6):
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
    new_cells = np.full(cells.shape, False, dtype=bool)
    max_x = cells.shape[0]
    max_y = cells.shape[1]

    for ix, iy in np.ndindex(cells.shape):
        count = 0
        #count neighbors
        for x in range(-1,2):
            for y in range(-1,2):
                #skip self (0,0)
                if not (x == 0 and y == 0):
                    #count off the map as True
                    if x+ix >= max_x or y+iy >= max_y or x+ix < 0 or y+iy < 0:
                        count += 1
                    #iterate counter if true
                    elif(cells[ix+x,iy+y]):
                        count += 1
        #if Cell is "live" checks
        if cells[ix,iy]:
            #Kill if isolated
            if count < min_neighbors:
                new_cells[ix,iy] = False
            #Kill if overcrowded
            elif count > max_neighbors:
                new_cells[ix,iy] = False
            #Else Live
            else:
                new_cells[ix,iy] = True
        #If cell is dead checks if neighors are exactly 3 and revives
        elif not cells[ix,iy] and count == 3:
            new_cells[ix,iy] = True
        #hard contain map edges
        if ix == 0 or iy == 0 or ix == max_x or iy == max_y:
            new_cells[ix,iy] = True
    return new_cells
    