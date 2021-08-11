#! python3
from termcolor import colored
import sys
import os
import random
from time import sleep 
from colorama import init
init()

# get all the avaliable flashcards
list_of_flashcards = []
for i in os.listdir(os.path.dirname(os.path.realpath(__file__))):
    if i.endswith(".txt"):
        list_of_flashcards.append(i)

# Introduction + settings
print(chr(27) + "[2J") # clear the console
print("\033[%d;%dH" % (0, 0)) # move the cursor position to (0,0) 
print(colored("Welcome to Flashcards!","green")+"\n\n")
print(colored("What flashcard do you want to open?", "cyan"))
print(colored("Avaliable Flashcards: ","cyan"),end="") 
if len(list_of_flashcards) == 0:
    raise Exception("No flashcards found!")    
for i in list_of_flashcards:
    print(i[0:-4], end=" ")
print("") 
filename = input("")
while filename + ".txt" not in list_of_flashcards:
    if filename.strip() == "exit" or filename.strip() == "Exit":
        print(colored("Program Terminated", "red"))        
        exit(0)
    print(colored("Invalid flashcard name. Try Again: ","cyan"))
    filename = input("")
print(colored("Should we ask you to compare answer to your response? (y/n) ","cyan"))
should_ask = True if input("") == "y" else False
print(colored("Should we ask not only the questions but also the answers? (y/n) ","cyan"))
should_quest = True if input("") == "y" else False
print(colored("Great! Let's begin!", "green"))
sleep(1)

# try to open the txt file, if we can't throw error
flashcards = {}
try:
    f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), filename + ".txt"))
    value = ""
    key = ""
    for line in f.readlines():
        # remove any \n from the end of the line
        line = line.rstrip()
        if line[0] == "#":
            continue
        if key == "":
            key = line 
        else:
            value = line
            flashcards[key] = value
            if should_quest:
                flashcards[value] = key 
            value = ""
            key = ""
    f.close()
except IOError:
    raise Exception("File not found.")

# evaluate flashcards 
if len(flashcards) == 0:
    raise Exception("Flashcards are empty. Make sure that your text file has more than 1 line!")
if "exit" in flashcards.values():
    raise Exception("Don't use 'exit' in your flashcards!")

# test user with flashcards
unknown = list(flashcards.keys())
familiar = []
mastered = []
shaky = [] 
while True:
    print(chr(27) + "[2J") # clear the console
    print("\033[%d;%dH" % (0, 0)) # move the cursor position to (0,0) 
    # check if user has mastered all cards
    if len(flashcards) == len(mastered):
        print(colored("Congratulations! You have mastered all of your cards!","green"))
        exit(0)

    # Show progress
    print(colored("Unknown:  " + str(len(unknown)), "red"))
    print(colored("Shaky:    " + str(len(shaky)),"blue"))
    print(colored("Familiar: " + str(len(familiar)), "yellow"))
    print(colored("Mastered: " + str(len(mastered)), "green"))
    print("\n\n")

    # Show Question
    print(colored("Question:", "cyan"), end=" ")
    index = random.randint(0,len(unknown) + len(familiar) - 1)
    question = unknown[index] if index < len(unknown) else familiar[index - len(unknown)]
    answer = flashcards[question]
    print(question + "\n")
    
    # Question user
    print(colored("Your Response:","cyan"), end=" ")
    response = input("")
    if response.strip() == "exit" or response.strip() == "Exit": 
        print(colored("Program Terminated","red"))
        exit(0) 
    elif response.lower().strip() == answer.lower().strip():
        print(colored("Correct!","green"))
        if index < len(unknown):
            familiar.append(unknown.pop(index))
        else:
            mastered.append(familiar.pop(index - len(unknown)))
    else:
        did_fail = None
        if not should_ask: 
            did_fail = True
        else: 
            print("")
            if response != "" and response != " ":
                print(colored("Answer:        ", "cyan") + answer)
                print(colored("Is this correct? (Answer truthfully! y/n):", "cyan"),end=" ")
                is_correct_input = input("")
                if is_correct_input == "y":
                    did_fail = False
                else:
                    did_fail = True
            else:
                print(colored("Answer: ", "cyan") + answer)
                input(colored("Press enter to continue", "cyan"))
                did_fail = True

        if did_fail:
            print(colored("Incorrect!", "red"))
            # add to shaky 
            if index in shaky:
                unknown.append(familiar.pop(index - len(unknown)))
                shaky.pop(index)
            elif index >= len(unknown):
                shaky.append(index)
        else:
            print(colored("Correct!","green"))
            if index < len(unknown):
                familiar.append(unknown.pop(index))
            else:
                mastered.append(familiar.pop(index - len(unknown)))
    sleep(1)
