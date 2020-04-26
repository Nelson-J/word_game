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
from time import time
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

    return user_input #handle input

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

    return word_list #convert the string of dictionary words to a scannable list

dictionary_word_list = dictionary_string_to_list(dictionary)

def word_exists(word):
    """
    Function verifies that the word exists in a dictionary (loaded from a file).
    return True or False
    """
    #verify word existence from loaded dictionary
    if(word in dictionary_word_list):
        dictionary_word_list.remove(word) #ensures that same word isn't entered multiple times
        return True
    return False

def get_accuracy(word, random_string):
    """
    Function to Calculate how accurate the Player response is,
    based on the number of letters used from the generated string of characters
    If the player includes a letter which isn't in the string, accuracy given is 0
    - used in grading
    """
    letters_present = 0
    random_string_length = len(random_string)

    for letter in word:
        if(letter in random_string):
            letters_present = letters_present + 1
            accuracy = (letters_present/random_string_length)*100
        else:
            return 0
    return accuracy

def grade(accuracy):
    """
    Grader
    Function to grant user points based on their accuracy
    """
    accuracy = int(accuracy)
    if(accuracy == 0):
        points = 0
    elif(accuracy in range(1, 30)): # 0 - 29
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


# ======================== Handling how user could get optimal points ==========================================

def sub_words(random_string): #return all possible words that can be formed from string of characters
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

def grade_word_list(word_list):
    """
    Function gets a word list with accuracies and transforms these accuracies to points
    """
    for key, value in word_list.items():
        word_list[key] = grade(value)
    return word_list # identify the points that go for the sub_words' accuracies

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

def point_distribution (word_list):
    """
    Function gives the point distribution of words, in word_list
    i.e. given a list of words, it returns how many words have each point available,
    where the word_list is a dictionary of words and their corresponding point value
    """

    points_distribution = {2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0}
    point = 1
    frequency = 0
    for value in word_list.values():
        #for each point
        for key_point, value_point in points_distribution.items():
            #get the corresponding point and increase its frequency
            if value == key_point:
                value_point = value_point+1
                points_distribution[key_point] = value_point

    #do not store a point that isn't present in the list-----------------------------------------------------

    return points_distribution

def get_words_with_point(word_list, point):
    """
    Function returns words that have a given point value
    - Takes a list of words with assigned point values
    """
    words = []

    for key, value in word_list.items():
        if int(value) == point:
            words.append(key)
    return words

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

def is_present(word, word_list):
    """
    Function verifies that word is present in given list

    -Input: a word As String
            a list or words As List or Dictionary
    -Output: Boolean
    """
    if word in word_list:
        return True
    else:
        return False


# ============================================= WORD GAME =================================================================

#user combination
separator = "============================================================================================================="
print(separator)
print("This is a word game. \nThe idea is inspired from a past(?) TV show. \nPlayers request for a combination of consonants and vowels, which are given at random.\nThey then have to make top scoring words from the given combination")
print("\nHow To Play: Request a random combination of vowels and consonants \nWith c = consonant and v = vowel ")
print(separator)

combination = input("\nEnter a combination (e.g. ccvc) : ")
combination = sterilise_input(combination)

#generate random string and print
random_string = generate_word(combination)
print(random_string.upper())

#get all possible words that can be made from random_string
all_subwords = sub_words(random_string)
all_subwords_with_point_value = grade_word_list(all_subwords) #give each word the appropriate point

players_guess = {}#keep track of  words that player has guessed right

#Permit user to enter multiple words whose points will be added to award their final points
twenty_five_seconds_ahead = time() + 25
total_points = 0
accuracy = 0

# 25 seconds game time
while (twenty_five_seconds_ahead-time()) > 0:

    #print time
    print(str(int(twenty_five_seconds_ahead - time()))+" seconds left")

    #user guesses
    user_word = input("\nEnter your guess: ") #user guess
    user_word = sterilise_input(user_word)

    #word is verified by checking that it is present in the subword list
    #present? the point is awarded
    #Not present a 0 point is awarded
    if is_present(user_word, all_subwords):
        points = all_subwords.pop(user_word) #remove played guess to avoid giving points on second entry
        players_guess[user_word] = points #keep record of played guess
    else:
        points = 0

    print("Points = "+str(points))

    #sum points of individual words
    total_points = total_points + points



#---- Maximum Points----

#Finding the word that would yield the maximum number of Points
subwords_left = sub_words(random_string)
best_word = word_with_max_points(subwords_left)

#Get the number of points the best word would yield
best_accuracy = get_accuracy(best_word, random_string)
best_points = award_points(best_word, best_accuracy)

if accuracy == best_accuracy:
    print("Excellent !!! - You had a word with highest points!")

#--- At the end of the game
print("\nYou made "+ str(total_points)+" points !!")

print("\nBest Word")
print(best_word.upper()+" --with-- "+ str(best_points)+" Points")
