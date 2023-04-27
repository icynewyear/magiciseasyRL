from __future__ import annotations

from typing import TYPE_CHECKING

import tcod
from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov
from game_state import GameState

from input_handlers import MainGameEventHandler
from render_functions import render_bar, task_menu, ponder_menu
from message_log import MessageLog

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap
    from input_handlers import EventHandler

class Engine:
    game_map: GameMap

    def __init__(self, player: Actor):
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.message_log = MessageLog()
        self.player = player
        self.state = GameState.LOOP

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=5,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:

        self.game_map.render(console)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        #HP Display
        render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        task_menu(
            console=console
        )
        if self.state == GameState.PONDER:
            input = ""
            ponder_menu(console=console, input=input)
            while self.state == GameState.PONDER:
                context.present(console)
                console.clear()
                key = tcod.console_wait_for_keypress(True)
                if key.vk == tcod.KEY_ENTER or key.vk == tcod.KEY_KPENTER:
                    ponder_menu(console=console, input=input)
                    context.present(console)
                    console.clear()
                    self.state = GameState.LOOP
                elif key.vk == tcod.KEY_BACKSPACE:
                    input = input[:-1]
                elif key.c:
                    input += chr(key.c)
                ponder_menu(console=console, input=input) 
            
        context.present(console)

        console.clear()
