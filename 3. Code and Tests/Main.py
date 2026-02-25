import os

def test():
    print("The test function was called.")
def settings(): #it is starting to occur to me that I really should have used a proper CLI library.
    # colour_list = { #if I end up using this, I have to import all the colours as a
    #     '1': colour1,
    #     '2': colour2,
    #     '3': colour3,
    #     '4': colour4,
    #     '5': colour5,
    #     '6': colour6,
    #     '7': colour7,
    #     '8': colour8
    # }
    sound_enabled = True
    def sound_settings():
        os.system('cls' if os.name == 'nt' else 'clear')
        answer = input('Would you like to DISABLE game sounds? (Y/N)')
        if answer.casefold() == 'y':
            sound_enabled = False
            return sound_enabled

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
    if option == 2:  # Does this work? '2'?
        sound_settings()

    # TODO: Rethink the entire way i was planning to do colours.

    # elif option == "1": #There are so, so many ways to do this, I am sure. All of them would be better than this abomination.
    #     print(f'''
    #     Colour customisation:
    #
    #     [1]: Colour of number one (Currently {colour1})
    #     [2]: Colour of number two (Currently {colour2})
    #     [3]: Colour of number three (Currently {colour3})
    #     [4]: Colour of number four (Currently {colour4})
    #     [5]: Colour of number five (Currently {colour5})
    #     [6]: Colour of number six (Currently {colour6})
    #     [7]: Colour of number seven (Currently {colour7})
    #     [8]: Colour of number Eight (Currently {colour8})
    #
    #     [R]: Return
    #     ''')
    #     option = input()
    #     new_colour = input(f'What would you like to change {option} to? (red, green, yellow, etc)')
    #     colour_list.get(option)

    elif option.casefold() == 'R':
        return(sound_enabled) #Returns the values of all the settings for use elsewhere.


dispatch_table = { #The dispatch table should contain an entry of every command that can be called.
    "test": test,
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

