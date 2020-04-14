"""
Word-Guess game (work in progress)
- program gets the length of entered word and generates a random string of words
    based on a consonant (c) - verb (v) combination
Final product:
- Given a c-v combination game generates a random string
- Player uses generated string to build a correct english word
- Points (0 - 10) are awarded based on the number of letters used from the generated string, to build the word
- In the end, computer gives the word(s) that would give the greatest Points

More details... see About_Game file
"""
from word_generator import *
"""
Algo-1:
1 - Store a word (random_string).
2 - Generate a random string - (t = total number to letters).
3 - Get the number of letters in the stored word that are present in the generated string (= n)
4 - Calculate the accuracy(?) - [(n/t)*100]
  - The accuracy is used in grading
"""

#load required dictionary
file = open("dictionary.txt", "r")
dictionary = file.read()

def dictionary_string_to_list(dictionary):
    """
    Function converts dictionary string into a list of dictionary words
    """
    content = dictionary
    word = ""
    word_list = []

    for letter in content:
        if(letter != "\n"):
            word = word.__add__(letter)
        else:
            word_list.append(word)
            word = ""

    return word_list

dictionary_word_list = dictionary_string_to_list(dictionary)

def get_accuracy(word, random_string):
    """
    Function to Calculate how accurate the Player response is,
    based on the number of letters used from the generated string of characters
    - used in grading
    """
    letters_present = 0
    random_string_length = len(random_string)

    for letter in word:
        if(letter in random_string):
            letters_present = letters_present + 1
            accuracy = (letters_present/random_string_length)*100
    return accuracy

def grade(accuracy):
    """
    Grader
    Function to grant user points based on their accuracy
    """
    accuracy = int(accuracy)
    if(accuracy in range(0, 30)): # 0 - 29
        points = 2
    elif(accuracy == 30):
        points = 3
    elif(accuracy in range(31, 50)): # 31 - 49
        points = 4
    elif(accuracy == 50):
        points = 5
    elif(accuracy in range(51, 80)): # 51 - 79
        points = 7
    elif(accuracy == 80):
        points = 8
    elif(accuracy in range(81, 100)): # 81 - 99
        points = 9
    elif(accuracy == 100):
        points = 10
    else:
        points = 0
    return points

def award_points(word, accuracy):
    """
    Function awards points based on the existence of the word entered
    If word does not exist, 0 is awarded
    """
    if(word_exists(word)):
        return grade(accuracy)
    return 0

def sterilise_input(user_input):
    """
    Fuction cleanses user input
    """
    #lowercase
    user_input = user_input.lower()
    user_input = user_input.strip() # remove whitespaces

    #ensure that input is letter
    for letter in user_input:
        if letter.isalpha() == False:
            print("Unknown character detected, Please Try Again")
            exit()

    if(user_input == ""):
        print("Try Again")
        exit()

    return user_input

def sub_words(random_string): #print all possible words that can be formed from string of characters
    """
    Function finds dictionary words that can be formed by letters in the random generated string
    """
    string_length = len(random_string)
    #sub_word_list = []
    sub_word_list = {}

    #take a dictionary word
    for word in dictionary_word_list:
        dictionary_word_length = len(word)

        #valid dictionary words can only have lengths that are less than or equal to the length of the string
        if dictionary_word_length > string_length:
            continue

        current_word = word # we want to keep the dictionary word unaltered
        letter_count = 0

        #take each letter in the random_string
        for letter in random_string:
            #does the dictionary_word have the random_string letter
            if(letter in current_word):
                letter_count = letter_count + 1 #if it does: count that letter as 1
                current_word = current_word.replace(letter,"",1)# delete that occurence, to allow checking for duplicates

        #we have the number of letters from the random_string that are present in the dictionary word - letter_count
        #if current_word remains with letters that are not in random_string, it isn't a valid sub word
        if len(current_word) != 0:
            continue

        percentage_accuracy = (letter_count / string_length) * 100
        sub_word_list[word] = round(percentage_accuracy, 2) #store word and 'accuracy' in dictionary

        #sub_word_list.append(word)
    return sub_word_list

def word_exists(word):
    """
    Function verifies that the word exists in a dictionary (loaded from a file).
    return True or False
    """
    #verify word existence from loaded dictionary
    if(word in dictionary_word_list):
        return True
    return False

def possible_best_words(possible_words):
    """
    Fuction determines and returns accurate words from the /dictionary/ of possible words(with accuracy)
    """
    max = 0
    best = {}

    for key, value in possible_words.items():
        if value > max:
            max = value
            best[key] = value
    return best

def word_with_max_points(possible_words):
    """
    Function returns the word that would have yielded the highest points
    """
    max = 0

    for key, value in possible_words.items():
        if value > max:
            max = value
            best = key
    return best

# ====================================== WORD GAME ===================================================================

#user combination
separator = "============================================================================================================="
print(separator)
print("This is a word game. \nThe idea is inspired from a past(?) TV show. \nPlayers request for a combination of consonants and vowels, which are given at random.\nThey then have to make top scoring words from the given combination")
print(separator)

combination = input("\nReqest a random combination of vowels and consonants \nWith c = consonant and v = vowel (e.g. ccvc) : ")
combination = sterilise_input(combination)

#generate random string and print
random_string = generate_word(combination)
print(random_string.upper())

#user guesses
user_word = input("\nEnter your guess: ") #user guess
user_word = sterilise_input(user_word)

#get accuracy, verify and grade
accuracy = get_accuracy(user_word, random_string)
points = award_points(user_word, accuracy) #grade
print("Points = "+str(points))

#Finding the word that would the maximum number of Points
all_subwords = sub_words(random_string)
best_word = word_with_max_points(all_subwords)

#Get the number of points the best word would yield
best_accuracy = get_accuracy(best_word, random_string)
best_points = award_points(best_word, best_accuracy)

if accuracy == best_accuracy:
    print("Excellent !!!")

print("\nBest Word")
print(best_word.upper()+" --with-- "+ str(best_points)+" Points")
