import os

#TODO: Something is seriously broken. I think that whatever we do in the symbol settings is obliterating the entire game settings.
game_settings = {
    "flag_symbol": "X",
    "mine symbol": "O",
}
def debug1():
    print("Debug 1 online")
    print(game_settings)
def settings(sound_enabled=None):
    def sound_settings():
        os.system('cls' if os.name == 'nt' else 'clear')
        answer = input('Would you like game sounds? (Y/N) ')

        if answer.casefold() == 'y':
            print("Sounds have been ENABLED.")
            input('Press enter to return to the settings menu.')
            return True
        elif answer.casefold() == 'n':
            print("Sounds have been DISABLED.")
            input('Press enter to return to the settings menu.')
            return False

        return None
    def symbol_settings(): #TODO: ensure that the default settings, and changes made to those settings, are all written into a file.
        os.system('cls' if os.name == 'nt' else 'clear')

        print(f'''
        Current symbols:
        
        flag_symbol: {game_settings["flag_symbol"]}
        Mine symbol: {game_settings["mine symbol"]}
        
        Type the name of the symbol you would like to change or press enter to return to the settings menu.
        ''')
        ui = input()
        if ui == "":
            return None
        elif ui not in game_settings:
            print("Invalid symbol name.")
            symbol_settings()
            return None
        else:
            print(game_settings[ui])
            editing_setting = ui
            new_value = input(f"Enter the new value for {editing_setting}: ")
            game_settings[editing_setting] = new_value

            print(f"The new value for {editing_setting} is {new_value}")
            settings() #TODO: See what this interferes with and ideally implement a cleaner way of returning to the homepage. Perhaps if we simply write the settings to a file, we don't need to worry about all of this anyhow.
            return None

    os.system('cls' if os.name == 'nt' else 'clear')
    print('''
    Settings:
    Choose a category:

    [1]: Colour customisation
    [2]: Sound options
    [3]: Symbol customisation

    [R]: Return
    ''')

    option = input()

    if option == "2":
        new_sound_value = sound_settings()
        if new_sound_value is not None:
            sound_enabled = new_sound_value
        return settings(sound_enabled)

    elif option == "3":
        symbol_settings()
    elif option == "1": # Do not ask why 1 comes after 3.
        print("Colour customisation not yet implemented.")

    elif option.casefold() == 'r':
        pass
    return None


dispatch_table = { #The dispatch table should contain an entry of every command that can be called.
    "settings": settings,
    "debug-1": debug1,
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
    def command_handler():
        command_input = input("Select an option or enter a command:\n")
        handler = dispatch_table.get(command_input) #Uses get to get the input command from the dispatch table.
        if handler: #Checks if the handler successfully called a command and produces an error if it was not.
            handler()
            return None
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
                    command_handler()
    command_handler()

difficulty=main_menu(1)
print(difficulty)