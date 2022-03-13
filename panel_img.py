import time
import random
from tracemalloc import start
from rich.live import Live
from rich.table import Table
from rich.console import Console
from rich.align import Align
from rich import box
from rich.pretty import pprint
import re

table = Table()

import cli
import img

console = Console()

cols, lines = cli.get_console_size()
lenght = cols // 8 * 4  

def img_repr(img):
    res = []
    for line in img.split('\n'):
        res_line = []
        for char in line:
            res_line.append(char)
        res_line.append('\n')
        res.append(res_line)
    return res

def replaced_img_repr(img, char_to_replace):
    res = []
    for line in img.split('\n'):
        res_line = []
        for char in line:
            res_line.append(char_to_replace)
        res_line.append('\n')
        res.append(res_line)
    return res


def get_gap():
    img_height = 0
    for line in img.logo.split('\n'):
        img_height +=1

    lines_coeff = lines - 10 - img_height
    return lines_coeff


def glitcher(line):
    for i in range(len(line)):
        if line[i]!='\n':
            line[i]=str(random.choice([0,1]))
    print(line)
    # console.log(type(line))
    return line

def updater(itteration, start, end):
    res = []
    for line in range(len(img.hangman)):
        print(start[line])
        if start[line]!=['\n']:
            start[line] = glitcher(start[line])
        console.log('--')
        # res.append(["[green]"]+end[line][:itteration]+["[/]"]+["[green dim]"]+start[line][itteration:]+["[/]"])
        res.append(end[line][:itteration]+start[line][itteration:])
    
    return res

def update_panel(itteration,start_img, end_img,caption, glitch=False):
    caption_text = "[purple]Loading...[/]"
    if caption:
        caption_text = '[purple]Completed.[/]'
    table = Table(show_header=False,caption=caption_text, show_edge=True, border_style="purple dim",box=box.ROUNDED)


    # if glitch :
    #     for i in range(len(start_img)):
    #         start_img[i]=str(random.choice([0,1]))

    # seconde phase shift un_updated image 
    end_img = updater(itteration=itteration, end=end_img, start=start_img)

    # final phase transforming list of lists in string
    res = []
    for line in end_img:
        line = "".join(line)
        res.append(line)
    res =''.join(res)

    table.add_row(f"{res}")
    table = Align(table,align="center")
    return table

def draw(img_id):
    start_img = replaced_img_repr(img.hangman[img_id],'*')
    end_img = img_repr(img.hangman[img_id])
    with Live(console=console,auto_refresh=False) as live:  # update 4 times a second to feel fluid
        for i in range(img.hangman['length']+3):
            caption = False
            if i == len(start_img):
                caption = True
            live.update(update_panel(i, start_img, end_img, caption),refresh=True)
            time.sleep(.1)  # arbitrary delay


try:       
    draw(0)
except Exception:
    console.print_exception(show_locals = True)