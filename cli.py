from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.padding import Padding
from rich.align import Align
from rich.layout import Layout
from rich import print
from random import *
import os 
import sys
import time
from exc import CustomException


console = Console(highlight=False)


def get_console_size():
    '''returns current console size'''
    size =  os.get_terminal_size()
    cols = size.columns
    lines = size.lines
    return cols, lines


def get_padding(msg, vertical='top', align='center'):
    '''
        returns padding size
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


def compose_string(s, *args):
    '''returns string s with %var% replaced by arguments from *args.'''
    
    if args:
        for a in args:
            s = s.replace("%var%", a, 1)
            # console.log('replaced //', s, '//')
    else:
        raise CustomException("args are required")
    # console.log("compose string", "//",s,"//", ' -- return')
    return s


def printer_by_lett(msg, style='', align='center',vertical="top", timing=0.075):
    '''
        prints message msg letter by letter
        gets: align    -- x positionement 
              vertical -- y positionement !!possible only with clearing console 
              timing   -- time to wait between line printings
              style    -- additional apperance settings
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
        gets: align -- x positionement 
              timing  -- time to wait between line printings
              style   -- additional apperance settings
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
        
def prompt(msg, vertical='top', align='center', clear= False):
    '''handles Confirm.ask apperance'''
    manual_align(msg,align=align, vertical=vertical, clear=clear)
    return Confirm.ask(msg)


def echo(msg, align='r',style=''):
    col_coeff, line_coeff = get_padding(msg, align=align)   
    # console.log(col_coeff,cols, len(m),m)
    console.print(Padding(msg,(line_coeff, col_coeff)))
    # time.sleep(4)
    return
    
    

def multiline_echo(m, align='r',style=''):
    '''same as echo but for more then 1 line.'''
    lines = m.split('\n')
    for line in lines:
        echo(line, align, style)


def exit_conf():
    '''Confirm exit choice.'''
    conf = Confirm.ask('Do you want to exit?')
    if conf:
        console.print("Exited from user input")
    return True

