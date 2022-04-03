import time, os, random, re

from rich.console import Console

from exc import CustomException

import img
import cli
import loader
import panel_img

console = Console()


pattern = re.compile('[A-Z]')

# WORDS = ("python", "programming", "dictionnary", "editor", "list", "function")
WORDS = ("q")
    

def set_word(words):
    """ Returns random word from WORDS list """
    return random.choice(words)

def create_repr(word):
    """ Creates word representation in format: '_ _ _ _ _ _' """
    word_repr = ""
    for i in range(len(word)):
        word_repr += '_'
    return word_repr

def update_repr(word,current_repr, guess):
    """ Replaces ' _ ' to a letter  """
    current_repr = list(current_repr)
    ind = 0
    for let in word:
        if let == guess:
            current_repr[ind] = let
        ind += 1
    return current_repr


def status_logger(hp, turns, guessed_word, wrong_letters):
    print('\n'*3)
    panel_img.draw(hp)
    print('\n')
    cli.printer_by_lett(f"Turn # {turns}", style="green")
    cli.printer_by_lett(f"Guessed word -- {' '.join(guessed_word)}", style="green")
    cli.printer_by_line(f"Wrong letters : {' - '.join(wrong_letters)}", style="magenta")
    col, lines = cli.get_console_size()
    print('\n'*(lines//2-20))

# TODO: docstrings
def correct_letter_handler(word, guess, guessed_word):
    print('\n')
    cli.printer_by_lett("Succeed!", style="cyan")
    guessed_word = update_repr(word, guessed_word, guess)
    time.sleep(2)
    os.system('cls')
    return guessed_word
    
def wrong_letter_handler(guess, wrong_letters, hp):
    wrong_letters.append(guess)
    hp -= 1
    print('\n')
    cli.printer_by_lett("Nop!", style="magenta")
    time.sleep(2)
    os.system('cls')
    return wrong_letters, hp

    
def main():
    '''
        hp -- heat points
        turns -- how many turns passed
        wrong_letters -- wrong_letters list
        word -- word to guess
        guessed_word -- representation of already guessed part of word [ 'w_rd' ]   _
        guess -- current letter entered by user that supposed to be in word
    '''
    #TODO: maybe create a dict of properties ( class 'self' interpretation)
    hp = 7
    turns = 0
    wrong_letters = []
    try:
        word = set_word(WORDS)
        guessed_word = create_repr(word)
        cli.printer_by_lett(msg="Guessing started...", vertical='center', style="green")
        time.sleep(2)
        os.system('cls')
        while True:
            status_logger(hp=hp, guessed_word=guessed_word, turns=turns, wrong_letters=wrong_letters)
            print(' '*4,end='')
            guess = cli.prompt("[green]Try one letter[/]",type="question") # User input TODO: protect this
            # Exit check
            if len(guess) != 1:
                if guess.capitalize() != pattern:
                    print(' '*4,end='')
                    cli.printer_by_lett('Enter one letter!', style='magenta')
                    time.sleep(2)
                    os.system('cls')
                    continue
            if guess == "-e" or guess == "--exit":
                    if cli.exit_conf(): return
            # if correct
            if guess in word:
                guessed_word = correct_letter_handler(word, guess, guessed_word)
            #  if wrong
            else:
                wrong_letters, hp = wrong_letter_handler(guess, wrong_letters, hp) #TODO: unfinished function 
                if hp==0:
                    return
            # finish check
            if '_' not in guessed_word:
                cli.printer_by_lett(f"Finished",style='')
                cli.printer_by_lett(f"The word was - \"{word}\"",style='')
                time.sleep(3)
                return
            turns +=1 
            # return
    except CustomException:
        console.print_exception(show_locals = True)



# TODO black screen at start 
if __name__ == "__main__":
    cols, lines = cli.get_console_size()
    os.system('cls')
    start = cli.prompt('[green]Start Game[/]',vertical='center', type='confirm',clear=True)
    time.sleep(2)
    os.system('cls')
    if start:
        cli.printer_by_line(img.logo, style="green blink")
        loader.load()
        time.sleep(3)
        os.system('cls')
        main()
    