#! python3
from termcolor import colored
import sys
import os
import random
from time import sleep 
from colorama import init
init()

def should_close (response): 
    if response.lower().strip() == "exit":
        print(colored("Program Exited!", "red"))
        exit(0)
    return response

def ask_if_correct (response, answer, should_indent=True):
    is_correct = None
    if response != "" and response != " ":
        if should_indent: 
            print(colored("Answer:        ", "cyan") + answer)
        else: 
            print(colored("Answer: ", "cyan") + answer)
        is_correct_input = input(colored("Are your correct? (Answer truthfully! y/n): ", "cyan"))
        while is_correct_input != "y" and is_correct_input != "n": 
            should_close(is_correct_input)
            is_correct_input = input(colored("Invalid response, try again: ","cyan"))
        if is_correct_input == "y":
            is_correct = True
        else:
            is_correct = False
    else:
        print(colored("Answer: ", "cyan") + answer)
        should_close(input(colored("Press enter to continue (Enter 'exit' if you want to quit) ", "cyan")))
        is_correct = False
    return is_correct

def mark_correct (index, familiar, mastered):
    print(colored("Correct!", "green"))
    if index < len(unknown): 
        familiar.append(unknown.pop(index))
    else: 
        mastered.append(familiar.pop(index - len(unknown)))

def mark_incorrect (index, unknown, familiar, shaky):
    # add to shaky 
    print(colored("Incorrect!", "red"))
    if index in shaky:
        unknown.append(familiar.pop(index - len(unknown)))
        shaky.pop(index)
    elif index >= len(unknown):
        shaky.append(index)
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
    should_close(filename)
    print(colored("Invalid flashcard name. Try Again: ","cyan"))
    filename = input("")

print(colored("Should we ask you the answers along with the questions? (y/n)", "cyan"))
should_quest = input("")
while should_quest != "y" and should_quest != "n": 
    should_close(should_quest)
    print(colored("Invalid Response! Try again: ", "cyan"))
    should_quest = input("")
should_quest = True if should_quest == "y" else False

print(colored("Which mode? ","cyan") + "Text, Text->Flashcards, Flashcards")
mode = input("")
while mode != "Text" and mode != "Text->Flashcards" and mode != "Flashcards":
    should_close(mode)
    print(colored("Invalid mode. Try again: ", "cyan"))
    mode = input("")
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
    result = None
    if mode == "Flashcards":
        should_close(input(colored("Press enter when you are ready to see the answer. Enter 'exit' if you want to quit. ", "cyan")))
        if ask_if_correct(None, answer, False): 
            mark_correct(index, familiar, mastered)
        else:
            mark_incorrect(index, unknown, familiar, shaky)
    else:
        print(colored("Your Response:","cyan"), end=" ")
        response = should_close(input(""))
        if response.lower().strip() == answer.lower().strip():
            mark_correct(index, familiar, mastered)
        elif mode == "Text->Flashcards": 
            if ask_if_correct(response, answer):
                mark_correct(index, familiar, mastered)
            else:
                mark_incorrect(index, unknown, familiar, shaky)
        else: 
            mark_incorrect(index, unknown, familiar, shaky)
    
    sleep(1)
