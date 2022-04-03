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
END_CHAR = '█'
cols, lines = cli.get_console_size()
length = cols // 8 * 4  

def create_loader(l, char):
    res = []
    for i in range(l):
        res.append(char)
    return res

start_loader = create_loader(length, START_CHAR)
end_loader = create_loader(length, END_CHAR)

def get_gap():
    img_height = 0
    for line in img.logo.split('\n'):
        img_height +=1

    lines_coeff = lines - 10 - img_height
    return lines_coeff


def update_loader(iteration,start_loader, end_loader,caption):
    #caption 
    caption_text = "[green]Loading...[/]"
    if caption:
        caption_text = '[green]Completed.[/]'
        
    # initialize table
    table = Table(show_header=False,caption=caption_text, show_edge=True, border_style="green ",box=box.ROUNDED)
    
    # fill string with "1 0" 
    for i in range(len(start_loader)):
        start_loader[i]=str(random.choice([0,1]))
    
    # composing string 
    end_loader = ["[purple dim]"]+end_loader[:iteration]+[""]+start_loader[iteration:]+["[/]"]
    
    # adding composed string in table as row
    table.add_row("".join(end_loader))
    table = Align(table,align="center")
    return table

def load():
    print('\n'*get_gap())
    with Live(console=console,auto_refresh=False) as live:  # update 4 times a second to feel fluid
        
        for i in range(len(start_loader)+1):
            # caption handler     
            caption = False
            if i == len(start_loader):
                caption = True
                
            live.update(update_loader(i, start_loader, end_loader, caption),refresh=True)
            time.sleep(.1)  # arbitrary delay
        