import os 
import time
from random import *

from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.padding import Padding
from rich.align import Align
from rich.layout import Layout
from rich import print

from exc import CustomException


console = Console(highlight=False)


def get_console_size():
    '''returns current console size'''
    size =  os.get_terminal_size()
    return size.columns, size.lines


def get_padding(msg, vertical='top', align='center'):
    '''
        returns padding size (two integers corresponding to: number of newlines and number whitespace)
            msg -message needs for calculate message length
            vertical - vertical padding [t:top, c:center, b:bottom]
            align - vertical padding [l:left, c:center, r:right].
       '''
    cols, lines = get_console_size()
    if vertical == 'center':
        line_coeff = (lines - 3)// 2
    elif vertical == 'bottom':
        line_coeff = lines - 1
    else:
        line_coeff = 0
    if align== 'center':
        col_coeff = (cols  - len(msg))// 2
    elif align == 'right':
        col_coeff = cols - 1
    else:
        col_coeff = 0    
    return col_coeff, line_coeff


def manual_align(msg,align="center",vertical='top', clear=False):
    '''manually creates padding by printing whitespaces and newline characters'''
    col_coeff, line_coeff = get_padding(msg, vertical=vertical, align=align)   
    if clear:
        os.system('cls')
        print('\n'*line_coeff)
    print(' '*col_coeff, end='')


def printer_by_lett(msg, style='', align='center',vertical="top", timing=0.075):
    '''
        prints message msg letter by letter
        gets: align    -- x position 
              vertical -- y position !!possible only with clearing console 
              timing   -- time to wait between line printings
              style    -- additional appearance settings
    '''
    clear = True if vertical!="top" else False
    manual_align(msg, align=align, vertical=vertical, clear=clear)
    for i in msg:
        console.print(i, end='',style=style)
        time.sleep(timing)
    print('')
    return ''


def printer_by_line(msg, style='', align='center', timing=0.1):
    '''
        prints message msg line by line
        gets: align -- x position
              timing  -- time to wait between line printings
              style   -- additional appearance settings
              timing  -- time between print lines
    '''
    big_line = ''
    msg = msg.split('\n')
    for line in msg:
        if len(line) > len(big_line):
            big_line = line
    col_coeff, line_coeff = get_padding(big_line, align=align)
    for line in msg:
        console.print(Padding(line,(0,col_coeff), style=style))
        time.sleep(timing)
    return ''
        
def prompt(msg, type,vertical='top', align='center', clear= False):
    '''handles Confirm.ask appearance'''
    manual_align(msg,align=align, vertical=vertical, clear=clear)
    if type == 'confirm':
        # TODO: needs Prompt.ask support
        return Confirm.ask(msg)
    if type == 'question':
        # TODO: needs Prompt.ask support
        return Prompt.ask(msg)

def exit_conf():
    '''Confirm user's exit choice.'''
    conf = Confirm.ask('Do you want to exit?')
    if conf:
        console.print("Exited from user input")
    return True

