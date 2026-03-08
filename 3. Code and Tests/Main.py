import os
def settings(sound_enabled=None):
    def sound_settings():
        os.system('cls' if os.name == 'nt' else 'clear')
        answer = input('Would you like to DISABLE game sounds? (Y/N) ')

        if answer.casefold() == 'y':
            print("Sounds have been disabled.")
            input('Press enter to return to the settings menu.')
            return False
        elif answer.casefold() == 'n':
            print("Sounds have been enabled.")
            input('Press enter to return to the settings menu.')
            return True

        return None

    os.system('cls' if os.name == 'nt' else 'clear')
    print("Settings:")
    print('''
    Choose a category:

    [1]: Colour customisation
    [2]: Sound options
    [3]: Symbol customisation

    [R]: Return
    ''')

    option = input()

    if option == "2":
        new_value = sound_settings()
        if new_value is not None:
            sound_enabled = new_value
        return settings(sound_enabled)

    elif option.casefold() == 'r':
        return sound_enabled

    return None


dispatch_table = { #The dispatch table should contain an entry of every command that can be called.
    "settings": settings,
}

def main_menu(invoked_from): #This (mediocre) code checks if the main menu is being run on startup or midgame
                             # (if that ever happens, not sure why I would implement this), and changes the quit option accordingly.
    if invoked_from == "ingame":
        option = "Return"
        option_key = "R"
    else:
        option = "Quit"
        option_key = "Q"
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'''Welcome to minesweeper - terminal edition.
          Select a difficulty by entering the associated number, or enter a command.
          
          [1]: Easy
          [2]: Medium
          [3]: Hard
          
          [{option_key}]: {option}
          
          For information on how to play this game, and commands supported in this menu, type '?'.\n''')
    command_input = input("Select an option or enter a command:\n")
    handler = dispatch_table.get(command_input) #Uses get to get the input command from the dispatch table.
    if handler: #Checks if the handler successfully called a command and produces an error if it was not.
        handler()
    else:
        capitalised_input = command_input.capitalize() # allows the user to enter the quit option in any case.
        if capitalised_input == option_key:
            exit()
        else:
            try:
                val = int(command_input)
                return (
                    val)
            except ValueError:
                print("Command not recognised.")


difficulty=main_menu(1)
print(difficulty)

