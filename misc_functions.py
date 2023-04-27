from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from tcod import Console

import tcod

from render_functions import input_menu

def get_input(console: Console, prompt: str) -> str:
    input = ""
    while True:
        key = tcod.console_wait_for_keypress(True)
        if key.vk == tcod.KEY_ENTER or key.vk == tcod.KEY_KPENTER:
            return input
        elif key.vk == tcod.KEY_BACKSPACE:
            input = input[:-1]
        elif key.c:
            input += chr(key.c)
        pass