"""
File generates words based on an entered vowel-consonant pattern
-- Inspired from a tutorial (Building an interactive dictionary)---
"""
import string
import random

#global variables
vowels = ['a','e','i','o','u']
consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']

def is_vowel(letter):
    """
    Function determines if input letter is a vowel.
    """
    return letter in vowels

def is_consonant(letter):
    """
    Function determines if input letter is consonant.
    """
    return letter in consonants

def is_alphabet(letter):
    """
    Function determines it letter is of the alphabet
    """
    return is_vowel(letter) or is_consonant(letter) #applied OR rule :-)

def which(letter):
    """
    Function determines if letter is a vowel or a consonant.
    """
    if(is_vowel(letter)):
        verdict = "Vowel."
        return verdict
    elif(is_consonant(letter)):
        verdict = "Consonant."
        return verdict
    else:
        verdict = "None."
        return verdict

def generate_vowel():
    """
    Function generates a random vowel.
    """
    return random.choice(vowels)

def generate_consonant():
    """
    Function generates a random vowel.
    """
    return random.choice(consonants)

def generate_alphabet():
    """
    Function generates a random vowel.
    """
    return random.choice(string.ascii_lowercase)

def generate_word(combination):
    """
    Function generates a word based on the combination entered.
    """
    output = ''
    for letter in combination:
        if (is_alphabet(letter)):
            if(letter == 'c'):
                output = output + generate_consonant()
            elif(letter == 'v'):
                output = output + generate_vowel()
            else:
                output = output + letter
        else:
            print("Input is not a letter of the alphabet.")
    return output

def generate_words(combination, number=1): #!!! Issue: sequences terminate with a "None"!!!
    """
    Function gerates the number of words(strings) entered - 1 by default
    """
    for i in range(number):
        print(generate_word(combination))

def runMe():
    """
    Function launches the program.
    """
    print("\nEnter a combination of the following letters:\n - v For vowel \n - c For consonant\n - /your_letter/ For your choice of letter\ne.g. ccvc\n")
    combination = input("Your input: ")
    #number = input("Number: ")
    print(generate_words(combination))
