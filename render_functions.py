from __future__ import annotations

from typing import TYPE_CHECKING

import color

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

def ponder_menu(console: Console) -> None:
    console.print(
        x=95, y=30, string=f"What shall you ponder?", fg=color.bar_text
    )
    console.print(
        x=95, y=32, string=f"______________", fg=color.bar_text
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
