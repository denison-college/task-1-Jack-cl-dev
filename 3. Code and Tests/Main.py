import os

game_settings = {
    "flag_symbol": "X",
    "mine symbol": "O",
}
sound_enabled = True

game_colours = {
    "background": "black", #not sure if I can implement this, and if I can, not sure if I can do it like this.
    "text": "white",
    "flag": "red",
    "mine": "green",
    "title": "yellow",
    "mine_count": "blue",
    "timer_colour": "magenta"
}
def settings():
    global sound_enabled
    def sound_settings():
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            answer = input('Would you like game sounds? (Y/N, or press Enter to return) ')

            if answer == "":
                return None
            elif answer.casefold() == 'y':
                print("Sounds have been ENABLED.")
                input('Press enter to return to the settings menu.')
                return True
            elif answer.casefold() == 'n':
                print("Sounds have been DISABLED.")
                input('Press enter to return to the settings menu.')
                return False
            elif answer.casefold() == 'r':
                return None

            print("Invalid option.")
            input('Press enter to try again.')

    def symbol_settings():  # TODO: ensure that the default settings, and changes made to those settings, are all written into a file.
        global game_settings

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f'''
        Current symbols:

        flag_symbol: {game_settings["flag_symbol"]}
        mine symbol: {game_settings["mine symbol"]}

        Type the name of the symbol you would like to change.
        Press Enter or type R to return to the settings menu.
        ''')
            ui = input().strip()

            if ui == "" or ui.casefold() == "r":
                return None
            elif ui not in game_settings:
                print("Invalid symbol name.")
                input("Press enter to try again.")
            else:
                print(game_settings[ui])
                new_value = input(f"Enter the new value for {ui} (or press Enter to cancel): ")

                if new_value == "":
                    print("No changes made.")
                else:
                    game_settings[ui] = new_value
                    print(f'The new value for {ui} is {new_value}')

                input('Press enter to continue.')

    def colour_settings():
        global game_colours

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f'''
        Current colours:

        background: {game_colours["background"]}
        text: {game_colours["text"]}
        flag: {game_colours["flag"]}
        mine: {game_colours["mine"]}
        title: {game_colours["title"]}
        mine_count: {game_colours["mine_count"]}
        timer_colour: {game_colours["timer_colour"]}

        Type the name of the colour setting you would like to change.
        Press Enter or type R to return to the settings menu.
        ''')
            ui = input().strip()

            if ui == "" or ui.casefold() == "r":
                return None
            elif ui not in game_colours:
                print("Invalid colour setting name.")
                input("Press enter to try again.")
            else:
                print(game_colours[ui])
                new_value = input(f"Enter the new value for {ui} (or press Enter to cancel): ")

                if new_value == "":
                    print("No changes made.")
                else:
                    game_colours[ui] = new_value
                    print(f'The new value for {ui} is {new_value}')

                input('Press enter to continue.')

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('''
    Settings:
    Choose a category:

    [1]: Colour customisation
    [2]: Sound options
    [3]: Symbol customisation

    [R]: Return
    ''')

        option = input().strip()

        if option == "2":
            new_sound_value = sound_settings()
            if new_sound_value is not None:
                sound_enabled = new_sound_value

        elif option == "3":
            symbol_settings()

        elif option == "1":
            colour_settings()

        elif option.casefold() == 'r' or option == "":
            return None

        else:
            print("Invalid option.")
            input("Press enter to try again.")

dispatch_table = {  # The dispatch table should contain an entry of every command that can be called.
    "settings": settings,
}

def main_menu(invoked_from):  # This (mediocre) code checks if the main menu is being run on startup or midgame
                              # (if that ever happens, not sure why I would implement this), and changes the quit option accordingly.
    if invoked_from == "ingame":
        option = "Return"
        option_key = "R"
    else:
        option = "Quit"
        option_key = "Q"

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'''Welcome to minesweeper - terminal edition.
          Select a difficulty by entering the associated number, or enter a command.

          [1]: Easy
          [2]: Medium
          [3]: Hard

          [{option_key}]: {option}

          For information on how to play this game, and commands supported in this menu, type '?'.\n''')

        command_input = input("Select an option or enter a command:\n").strip()
        handler = dispatch_table.get(command_input)  # Uses get to get the input command from the dispatch table.

        if handler:  # Checks if the handler successfully called a command and produces an error if it was not.
            handler()
        else:
            capitalised_input = command_input.capitalize()  # allows the user to enter the quit option in any case.
            if capitalised_input == option_key:
                exit()
            else:
                try:
                    return int(command_input)
                except ValueError:
                    print("Command not recognised.")
                    input("Press enter to continue.")

difficulty=main_menu(1)
print(difficulty)