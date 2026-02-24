import os

def test():
    print("The test function was called.")

dispatch_table = { #The dispatch table should contain an entry of every command that can be called.
    "test": test,
}

def main_menu(invoked_from): #This (mediocre) code checks if the main menu is being run on startup or midgame
                             # (if that ever happens, not sure why I would implement this, and changes the quit option accordingly.
    if invoked_from == "ingame":
        option = "Return"
        option_key = "R"
    else:
        option = "Quit"
        option_key = "Q"
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Welcome to minesweeper - terminal edition.\n"
          "Select a difficulty by entering the associated number, or enter a command.\n"
          "\n"
          "[1]: Easy\n"
          "[2]: Medium\n"
          "[3]: Hard\n"
          "\n"
          f"[{option_key}]: {option}"
          "\n"
          "For information on how to play this game, and commands supported in this menu, type '?'.\n")
    input_command = input("Select an option or enter a command:\n")
    handler = dispatch_table.get(input_command) #Uses get to get the input command from the dispatch table.
    if handler: #Checks if the handler successfully called a command and produces an error if it was not.
        handler()
    else:
        print("Invalid command.")


main_menu(1) #This simply runs the main meny code for testing purposes



