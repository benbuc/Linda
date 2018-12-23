# Author: Benito Buchheim

# This Program is used to set up Linda
# You can create new services or remove services

import sys

def main():


    print("\nWhat do you want to do?")
    print("\t[1] List services")
    print("\t[2] Create new service")
    print("\t[3] Remove service")
    print("\t[0] EXIT")

    try:
        action = int(raw_input("Enter Action: "))
    except ValueError:
        print("Invalid input!")
        return

    print("")

    if action == 0:
        print("See you soon")
        sys.exit()
    elif action == 1:
        print("Listing services")
    elif action == 2:
        print("Creating new service")
    elif action == 3:
        print("Removing service")
    else:
        print("Unknown action")

    
if __name__ == "__main__":
    print("Hi, I am Linda. Have a great day")
    while "pigs" != "fly":
        main()