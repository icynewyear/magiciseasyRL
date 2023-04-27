from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

import color
import tcod

if TYPE_CHECKING:
    from tcod import Console

def action_menu(console: Console) -> None:

    pass

def task_menu(console: Console) -> None:
    console.print(
        x=95, y=5, string=f"Tasks", fg=color.bar_text
    )
    console.print(
        x=95, y=7, string=f"1: Howl at a god.", fg=color.bar_text
    )

def ponder_menu(console: Console, input: str) -> None:
    console.print(
        x=95, y=30, string=f"What shall you ponder?", fg=color.bar_text
    )
    console.print(
        x=95, y=32, string=input, fg=color.bar_text
    )
    
def option_menu(console: Console, header: str, options: list, width: int, fgcolor: tuple[int,int,int] = (0,0,0)):
    if len(options) > 26: raise ValueError("Cannot have a menu with more than 26 options.")
    
    #calculate height of header and options
    header_height = tcod.console_get_height_rect(console, 0, 0, width, console.height, header)
    height = len(options) + header_height
    
    #create an off-screen console that represents the menu's window
    window = tcod.console_new(width, height)
    
    #print the header, with auto-wrap
    tcod.console_set_default_foreground(window, fgcolor)
    tcod.console_print_rect_ex(window, 0, 0, width, height, tcod.BKGND_NONE, tcod.LEFT, header)
    
    #print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        tcod.console_print_ex(window, 0, y, tcod.BKGND_NONE, tcod.LEFT, text)
        y += 1
        letter_index += 1
        
    #blit the contents of "window" to the root console
    x = int(console.width/2 - width/2)
    y = int(console.height/2 - height/2)
    tcod.console_blit(window, 0, 0, width, height, console, x, y, 1.0, 0.7)
    
    #present the root console to the player and wait for a key-press
    tcod.console_flush()
    key = tcod.console_wait_for_keypress(True)
    
    #convert the ASCII code to an index; if it corresponds to an option, return it
    index = key.c - ord('a')
    if index >= 0 and index < len(options): return index
    
    return None

def input_menu(console: Console, prompt: str, input: str) -> None:
    console.print(
        x=95, y=30, string=prompt, fg=color.bar_text
    )
    console.print(
        x=95, y=32, string=input, fg=color.bar_text
    )
    
def render_bar(
    console: Console, current_value: int, maximum_value: int, total_width: int
) -> None:
    bar_width = int(float(current_value) / maximum_value * total_width)

    console.draw_rect(x=0, y=45, width=20, height=1, ch=1, bg=color.bar_empty)

    if bar_width > 0:
        console.draw_rect(
            x=0, y=45, width=bar_width, height=1, ch=1, bg=color.bar_filled
        )

    console.print(
        x=1, y=45, string=f"HP: {current_value}/{maximum_value}", fg=color.bar_text
    )
