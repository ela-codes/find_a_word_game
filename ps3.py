# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Aena Teodocio -- May 1, 2022
# Collaborators : <your collaborators>
# Time spent    : Roughly 5-7 hours. Lots of trial and error! :) Probably needs to be optimized.

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
WILDCARD = '*'

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
    'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0
}

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq


def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

    word: string
    n: int >= 0
    returns: int >= 0
    """
    if len(word) == 0:
        return 0

    the_word = word.lower()
    word_sum = 0

    for char in the_word:
        word_sum += SCRABBLE_LETTER_VALUES[char]

    total_score = word_sum * ((7 * len(the_word)) - (3 * (n-len(the_word))))

    if total_score <= -1:
        return word_sum
    else:
        return total_score


def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    displayed_hand = ''
    for letter in hand.keys():
        for j in range(hand[letter]):
            displayed_hand += letter + " "
    return displayed_hand


def deal_hand(n=7):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    count = 1
    hand = {}
    num_vowels = int(math.ceil(n / 3))
    
    if count == 1:  # include wildcard on first deal
        hand[WILDCARD] = 1
        count -= 1
        n -= 1

    # get random letters

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand


def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    my_hand = hand.copy()
    for char in word.lower():
        if char in my_hand and my_hand[char] > 0:
            my_hand[char] -= 1

    return my_hand


def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    my_word = word.lower()
    possible_word =[]
    if WILDCARD in my_word:
        for char in VOWELS:
            wc_word = my_word.replace(WILDCARD, char)
            if wc_word in word_list:
                possible_word.append(wc_word)
        if len(possible_word) == 0:  #if empty list, no matched words
            return False
    elif my_word not in word_list:
        return False

    # check if my_word is entirely composed of letters in hand
    my_hand = hand.copy()
    result = []
    for char in my_word:
        if char in my_hand and my_hand[char] == 0:
            result.append(False)
        elif char in my_hand and my_hand[char] != 0:
            my_hand[char] -= 1
            result.append(True)
        else:
            result.append(False)

    return all(result)


def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    count = sum([i for i in hand.values()])
    return count


def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    # Keep track of the total score

    # As long as there are still letters left in the hand:

    # Display the hand

    # Ask user for input

    # If the input is two exclamation points:

    # End the game (break out of the loop)

    # Otherwise (the input is not two exclamation points):

    # If the word is valid:

    # Tell the user how many points the word earned,
    # and the updated total score

    # Otherwise (the word is not valid):
    # Reject invalid word (print a message)

    # update the user's hand by removing the letters of their inputted word

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score

    # Return the total score as result of function

    n = calculate_handlen(hand)
    score = 0

    while n > 0:
        print('Current Hand:', display_hand(hand))
        word = input('Enter word, or "!!" to indicate that you are finished: ')

        if word == "!!":
            print('Total score for this hand: ' + str(score) + ' points')
            return score

        else:
            if is_valid_word(word, hand, word_list):  # if word is in word_list and letters used were in hand
                score_from_word = get_word_score(word, n)
                score += score_from_word
                hand = update_hand(hand, word)

                print('"' + word + '"' + ' earned ' + str(score_from_word) + ' points. Total: ' + str(score) + ' points')
                n = calculate_handlen(hand)

            else:  # invalid word
                print('That is not a valid word. Please choose another word.')
                # if any letters in hand were used in invalid word, remove it from hand
                hand = update_hand(hand, word)
                n = calculate_handlen(hand)

    print()
    print('Ran out of letters. Total score: ' + str(score) + ' points')
    return score


def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    del hand[letter]
    alphabet = (VOWELS + CONSONANTS).split()
    alphabet = ''.join([char for char in alphabet if char not in hand.keys()])
    curr_hand_length = calculate_handlen(hand)

    for i in range(7 - curr_hand_length):
        random_letter = random.choice(alphabet)
        hand[random_letter] = hand.get(random_letter, 0) + 1

    return hand


def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitute option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    total_score = 0
    HAND_SIZE = int(input('Enter total number of hands: '))
    hand = deal_hand()
    sub_count = 1
    replay_count = 1

    print('Current Hand:', display_hand(hand))

    while HAND_SIZE > 0:
        if sub_count == 1 and replay_count == 1:
            substitute = input('Would you like to substitute a letter? ').lower()
            if substitute in "yes":
                sub_letter = input('Which letter would you like to replace: ').lower()
                sub_count -= 1
                if sub_letter in hand:
                    hand = substitute_hand(hand, sub_letter)

        curr_score = play_hand(hand, word_list)
        total_score += curr_score
        HAND_SIZE -= 1
        print('----------')

        if replay_count == 1:
            replay = input('Would you like to replay the hand? ').lower()
            if replay in "no":
                hand = deal_hand()
                print('Current Hand:', display_hand(hand))
            if replay in "yes":
                HAND_SIZE += 1
                replay_count -= 1
                total_score -= curr_score

    print('Total score over all hands: ' + str(total_score))
    

if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
