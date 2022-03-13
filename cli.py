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

cols, lines = get_console_size()
width = cols // 8 * 4
height = lines // 8  * 6


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

def get_padding(msg, allign='t', justify='r'):
    '''
        returns padding size
            msg -message needs for calculate message length
            allign - vertical padding [t:top, c:center, b:bottom]
            justify - vertical padding [l:left, c:center, r:right].
       '''
    cols, lines = get_console_size()
    if allign == 'c':
        line_coeff = (lines - 3)// 2
    elif allign == 'b':
        line_coeff = lines - 1
    else:
        line_coeff = 0
    if justify== 'c':
        col_coeff = (cols  - len(msg))// 2
    elif justify == 'r':
        col_coeff = cols - 1
    else:
        col_coeff = 0    
    return col_coeff, line_coeff


def printer_by_lett(msg, style='', justify='left', timing=0.1):
    '''
        prints message msg letter by letter
        gets: justify -- x positionement 
              timing  -- time to wait between line printings
              style   -- additional apperance settings
    '''
    for i in msg:
        console.print(Align(line, style=style, align=justify))
        time.sleep(timing)
    return ''


def printer_by_line(msg, style='', justify='l', timing=0.1):
    '''
        prints message msg line by line
        gets: justify -- x positionement 
              timing  -- time to wait between line printings
              style   -- additional apperance settings
    '''
    big_line = ''
    msg = msg.split('\n')
    for line in msg:
        if len(line) > len(big_line):
            big_line = line
    col_coeff, line_coeff = get_padding(big_line, justify=justify)
    for line in msg:
        console.print(Padding(line,(0,col_coeff), style=style))
        time.sleep(timing)
    return ''
        

def echo(msg,m_type="normal", allign='t', justify='r',style='', clear_cli = False,*args,     **kwargs):
    '''
        clears console and prints message [m] of type [m_type] 
        in specified position allign : y, justify :x.
    '''
    if clear_cli:
        os.system('cls')
        
    col_coeff, line_coeff = get_padding(msg, allign=allign, justify=justify)     
    if m_type == "normal":
        # console.log(col_coeff,cols, len(m),m)
        console.log(args)
        if kwargs.by_printer:
            console.print(Padding(printer_by_lett(msg,style),(line_coeff, col_coeff)))
        else:
            console.print(Padding(msg,(line_coeff, col_coeff)))
        # time.sleep(4)
        return
    
    elif m_type == "ask":
        print('\n'*line_coeff)
        print(' '*col_coeff, end='')
        return Confirm.ask(msg)
    

def multiline_echo(m,m_type="normal", allign='t', justify='r',style='', clear_cli = False, **kwargs):
    '''same as echo but for more then 1 line.'''
    lines = m.split('\n')
    for line in lines:
        echo(line,m_type, allign, justify, style, clear_cli)


def exit_conf():
    '''Confirm exit choice.'''
    conf = Confirm.ask('Do you want to exit?')
    if conf:
        console.print("Exited from user input")
    return True

