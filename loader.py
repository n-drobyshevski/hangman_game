import time
import random
from rich.live import Live
from rich.table import Table
from rich.console import Console
from rich.align import Align
from rich import box

table = Table()

import cli
import img

console = Console()

START_CHAR = ' '
END_CHAR = '|'
cols, lines = cli.get_console_size()
lenght = cols // 8 * 5

def create_loader(l, char):
    res = []
    for i in range(l):
        res.append(char)
    return res

start_loader = create_loader(lenght, START_CHAR)
end_loader = create_loader(lenght, END_CHAR)

def get_gap():
    img_height = 0
    for line in img.logo.split('\n'):
        img_height +=1

    lines_coeff = lines - 10 - img_height
    return lines_coeff



def update_loader(itteration,start_loader, end_loader,caption, glitch=True):
    caption_text = "[purple]Loading...[/]"
    if caption:
        caption_text = '[purple]Completed.[/]'
    table = Table(show_header=False,caption=caption_text, show_edge=True, border_style="purple dim",box=box.ROUNDED)
    if glitch :
        for i in range(len(start_loader)):
            start_loader[i]=str(random.choice([0,1]))
    end_loader = ["[green]"]+end_loader[:itteration]+["[/]"]+["[green dim]"]+start_loader[itteration:]+["[/]"]
    table.add_row("".join(end_loader))
    table = Align(table,align="center")
    return table

def load():
    print('\n'*get_gap())
    with Live(console=console,auto_refresh=False) as live:  # update 4 times a second to feel fluid
        for i in range(len(start_loader)+1):
            caption = False
            if i == len(start_loader):
                caption = True
            live.update(update_loader(i, start_loader, end_loader, caption),refresh=True)
            time.sleep(.1)  # arbitrary delay
        