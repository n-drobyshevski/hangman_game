from email import message
import time 
import random
from rich.pretty import pprint
from rich.panel import Panel
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.align import Align
import os

from exc import CustomException
import cli
import img
import loader
import panel_img

console = Console()

WORDS = ("python", "programming", "dictionnary", "editor", "list", "function")
        
LOGS = {
    'START':"[bright_green]Guessing started..[/]",
    'GUESS':f"[blue]Turn #%var%[/]\n[blue]current word -- %var%[/]\n[bold red]Wrong letter %var%[/]"}        


def set_word(words):
    """ Returns random word from WORDS list """
    return random.choice(words)

def create_repr(word):
    """ Creats word representation in format: '_ _ _ _ _ _' """
    word_repr = ""
    for i in range(len(word)):
        word_repr += '_'
    return word_repr

def update_repr(word,current_repr, guess):
    """ Replaces ' _ ' to a letter  """
    ind = 0
    for let in word:
        if let == guess:
            current_repr = list(current_repr)
            pprint(type(current_repr))
            current_repr[ind] = let
            return current_repr
        ind += 1
    return current_repr


def logger(hp, turns, guessed_word, wrong_letters):
    print('\n'*3)
    # cli.printer_by_line(img.hangman[hp],style="green")
    panel_img.draw(hp)
    cli.printer_by_lett(f"Turn # {turns}", style="green")
    cli.printer_by_lett(f"Guessed word  -- {' '.join(guessed_word)}", style="green")
    cli.printer_by_line(f"Wrong letters -- {''.join(wrong_letters)}", style="red")

# TODO: docstrings
def correct_letter_handler(word, guess, guessed_word):
    console.print("Succes!", style="magenta")
    guessed_word = update_repr(word, guessed_word, guess)
    os.system('cls')
    return guessed_word
    
def wrong_letter_handler(guess, hp, wrong_letters):
    dead = False
    console.print("Wrong",style="red")
    os.system('cls')
    hp -= 1
    if guess not in wrong_letters:
        wrong_letters.append(guess)
    if hp == 0:
        print('you died...')
        dead = True
    return hp, wrong_letters, dead
    
def main():
    '''hp -- heat points
        turns -- how many turns passed
        wrong_letters -- wrong_letters list
        word -- word that u need to find
        guessed_word -- represen
        guess -- current suppossed letter 
        '''
    # TODO: guesses < turns
    hp = 7
    turns = 0
    wrong_letters = []
    try:
        word = set_word(WORDS)
        guessed_word = create_repr(word)
        cli.printer_by_lett(msg="Guessing started..", vertical='center', style="green")
        time.sleep(2)
        os.system('cls')
        while True:
            logger(hp=hp, guessed_word=guessed_word, turns=turns, wrong_letters=wrong_letters)

            guess = cli.prompt("[green]Try one letter[/]") # User input TODO: protect this
            if guess == "-e" or guess == "--exit":
                    if cli.exit_conf(): return
            if guess in word:
                guessed_word = correct_letter_handler(word, guess, guessed_word)
            else:
                hp, wrong_letters, dead = wrong_letter_handler(guess,hp, wrong_letters)
                if dead:
                    return
            if '_' not in guessed_word:
                console.print(f"Finished.\nThe word was - \"{word}\"")
                return 
            turns +=1 
    except Exception:
        console.print_exception(show_locals = True)

if __name__ == "__main__":
    cols, lines = cli.get_console_size()
    os.system('cls')
    # cli.multiline_echo(img.logo, style="green blink", justify='c', by_printer=False)
    start = cli.prompt('[green]Start Game[/]',vertical='center', clear=True)
    time.sleep(2)
    os.system('cls')
    if start:
        cli.printer_by_line(img.logo, style="green blink")
        loader.load()
        time.sleep(3)
        os.system('cls')
        main()
    