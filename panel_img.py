import time
import random

from rich.live import Live
from rich.table import Table
from rich.console import Console
from rich.align import Align
from rich import box
from rich.pretty import pprint


table = Table()

import cli
import img

console = Console(highlight=True)

cols, lines = cli.get_console_size()
length = cols // 8 * 4  

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
    ''' creates string with all characters replaced by char_to_replace'''
    res = []
    for line in img.split('\n'):
        res_line = []
        for char in range(len(line)):
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


def updater(iteration, start, end):
    res =[]
    for line in range(img.hangman["height"]):
        res.append(['[green]']+ end[line][:iteration]+['[/][green dim]']+start[line][iteration:]+['[/]'])
    # print(res)                  # uncomment
    
    return res 

def update_panel(iteration,start_img, end_img,caption,glitch=True):
    ### CAPTION CONFIG
    caption_text = "[purple]Loading...[/]"
    if caption:
        caption_text = '[purple]Completed.[/]'
        
    ### Initializing table
    table = Table(show_header=False,caption=caption_text, show_edge=True, border_style="purple dim",box=box.ROUNDED)

    ### Filling start_img with random chars 
    if glitch :
        for i in range(img.hangman["height"]):
            for char in range(img.hangman["length"]):
                if start_img[i][char] != '\n':
                    start_img[i][char]=str(random.choice([0,1]))
                             
    ### Seconde phase shift un_updated image 
    end_img = updater(iteration=iteration, end=end_img, start=start_img)

    #### Final phase transforming list of lists in string
    # Decomposing back to string

    res = [] 
    for line in end_img:
        line = "".join(line)
        res.append(line)
    res =''.join(res)

    table.add_row(f"{res}")
    table = Align(table,align="center")
    return table

def draw(img_id):
    end_img = img_repr(img.hangman[img_id])
    start_img = img_repr(img.hangman[img_id])
    # print(img.hangman[img_id])
    # pprint(end_img)
    with Live(console=console,auto_refresh=False) as live:  # update 4 times a second to feel fluid
        for i in range(img.hangman['length']+3):
            caption = False
            if i >= len(start_img)-1:
                caption = True
            live.update(update_panel(i, start_img, end_img, caption), refresh=True)
            time.sleep(.1)  # arbitrary delay
