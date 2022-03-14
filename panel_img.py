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

prev_line = []
def generate_steam(line_length, img):
    res = [] 
    # console.log('img len ',len(img))
    for line in range(len(img)):
        res_line = []
        # console.log('generator next line size', img[line])
        for char in img[line]:
            # console.log('qqqqqqqqqqqq', char)
            if char != '/n':
                res_line.append(str(random.choice([0,1])))
        # console.log('res_line', res_line)
        res.insert(-1, res_line)
        # console.log('res --', res)
    for line in res:
        print('res log --')
        pprint(line)
        yield res
    return

def glitcher(line, generator_obj):
    for line in generator_obj:
        yield line
    return

def updater(itteration, start, end, generator_obj):
    res = []
    for line in range(len(img.hangman)):
        # console.log('start line begin--', start[line])
        if start[line]!=['\n']:
            print('generator invoked')
            start[line] = generator_obj.__next__()
        # console.log('--')
        # console.log('start line --',start[line])
        # res.append(["[green]"]+end[line][:ietteration]+["[/]"]+["[green dim]"]+start[line][itteration:]+["[/]"])
        res.append(end[line][:itteration]+start[line][itteration:])
    
    return res

def update_panel(itteration,start_img, end_img,caption, generator_obj, glitch=False):
    caption_text = "[purple]Loading...[/]"
    if caption:
        caption_text = '[purple]Completed.[/]'
    table = Table(show_header=False,caption=caption_text, show_edge=True, border_style="purple dim",box=box.ROUNDED)


    # if glitch :
    #     for i in range(len(start_img)):
    #         start_img[i]=str(random.choice([0,1]))

    # seconde phase shift un_updated image 
    end_img = updater(itteration=itteration, end=end_img, start=start_img, generator_obj=generator_obj)

    # final phase transforming list of lists in string

    # adding missing newlines
    for i in end_img:
        for j in i:
            if type(j) == str:
                j = '\n'
            else:
                j.pop()
                j.append('\n')
    
    # copmposing
    res = []
    pprint(end_img)
    for line in end_img:
        line = line[0]
        # for sub in range(len(line)):
        #     line[sub] =''.join(line[sub])
            # print('sub --',sub)
        # print(type(line))
        print(" ".join(['1','3']))
        line = "".join(line)
        res.append(line)
    res =''.join(res)

    table.add_row(f"{res}")
    table = Align(table,align="center")
    return table

def draw(img_id):
    start_img = replaced_img_repr(img.hangman[img_id],'*')
    end_img = img_repr(img.hangman[img_id])
    stream = generate_steam(img= start_img, line_length=img.hangman['length'])
    # console.log(end_img)
    with Live(console=console,auto_refresh=False) as live:  # update 4 times a second to feel fluid
        for i in range(img.hangman['length']+3):
            caption = False
            if i == len(start_img):
                caption = True
            live.update(update_panel(i, start_img, end_img, caption,generator_obj=stream), refresh=True)
            time.sleep(.1)  # arbitrary delay


try:       
    draw(0)
except Exception:
    console.print_exception(show_locals = False)