from email import message
import time 
import random
from rich.pretty import pprint
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.align import Align
import os

from exc import CustomException
import cli
import img
import loader

console = Console()

WORDS = ("python", "programming", "dictionnary", "editor", "list", "function")
        
LOGS = {
    'START':"[green dim]Enter -e or --exit anytime to exit...[/]\n[bright_green]Guessing started..[/]",
    'GUESS':"[blue]Turn #%var%\ncurrent word -- %var%[/]\n[bold red]Wrong letter[/]"}        


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

# TODO: docstrings
def correct_letter_handler(word, guess, wrong_letters):
    console.print("Succes!", style="magenta")
    guessed_word = update_repr(word, guessed_word, guess)
    console.print(f"current word -- \"{' '.join(guessed_word)}\"\n\nwrong letters -- \"{','.join(wrong_letters)}\"")
    os.system('cls')
    return guessed_word
    
def wrong_letter_handler(guess, guessed_word, wrong_letters):
    dead = False
    console.print("Wrong",style="red")
    console.print(f"current word -- \"{' '.join(guessed_word)}\"\n\nwrong letters -- \"{','.join(wrong_letters)}\"")
    os.system('cls')
    guesses -= 1
    if guess not in wrong_letters:
        wrong_letters.append(guess)
    if guesses == 0:
        print('you died...')
        dead = True
    return guessed_word, wrong_letters, dead
    
def main():
    # TODO: guesses < turns
    guesses = 10
    turns = 0
    wrong_letters = []
    try:
        word = set_word(WORDS)
        guessed_word = create_repr(word)
        cli.multiline_echo(m=LOGS["START"],m_type='normal',allign='c',justify='c')
        while True:
            info_log = cli.compose_string(LOGS["GUESS"],f"{' '.join(guessed_word)}")
            cli.multiline_echo(m=info_log,m_type='normal',allign='c',justify='c')
            guess = Prompt.ask("Try one letter:") # User input TODO: protect this
            if guess == "-e" or guess == "--exit":
                    if cli.exit_conf(): return
            if guess in word:
                guessed_word = correct_letter_handler(word, guess, wrong_letters)
            else:
                guessed_word, wrong_letters, dead = wrong_letter_handler()
                if dead:
                    return
            if '_' not in guessed_word:
                console.print(f"Finished.\nThe word was - \"{word}\"")
                return 
            turns +=1
            print("===================================")   
    except Exception:
        console.print_exception(show_locals = True)

if __name__ == "__main__":
    cols, lines = cli.get_console_size()
    os.system('cls')
    # cli.multiline_echo(img.logo, style="green blink", justify='c', by_printer=False)
    start = cli.echo('[green]Start Game[/]', m_type='ask',allign='c', justify='c')
    time.sleep(2)
    os.system('cls')
    if start:
        cli.printer_by_line(img.logo, justify='c', style="green blink")
        loader.load()
        time.sleep(3)
        # os.system('cls')
        main()
    