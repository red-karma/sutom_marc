import string
import copy

def read_file_dict(filename='pli07.txt'):
    with open(filename) as file:
        words = [line.rstrip() for line in file]
    return words


def keep_words_with_len(words, word_len):
    possible_words = [word for word in words if len(word) == word_len]

    if len(possible_words) == 0:
        raise Exception(f"There is no word with size '{word_len}' in the dictionary")

    return possible_words


def does_word_contain_known_letter(word, letter, position):

    if position > len(word):
        # Sanity check: the position of the letter should not be bigger than the size of the word (!!)
        raise Exception(f"Position '{position}' of letter '{letter}' is bigger than the word size '{len(word)}'")

    return word[position - 1] == letter

def keep_words_with_known_letter(words, letter, position):
    possible_words = [word for word in words if does_word_contain_known_letter(word, letter, position)]
    return possible_words


def detect_possible_possible_position_for_wrong_place_letter(word, already_taken_positions_by_letter, letter, wrong_position):
    if wrong_position > len(word):
        # Sanity check: the position of the letter should not be bigger than the size of the word (!!)
        raise Exception(
            f"Position '{wrong_position}' of letter '{letter}' is bigger than the word size '{len(word)}'")

    # The letter at position 'wrong_position' must NOT be 'letter'
    if word[wrong_position - 1] == letter:
        return 0

    # But the word should contain this letter somewhere else, if the letter was not already taken into account
    possible_position = -1
    for letter_position in range(0, len(word)):
        if letter == word[letter_position] and letter_position not in already_taken_positions_by_letter[letter]:
            possible_position = letter_position

    return possible_position + 1


def is_word_possible(word, already_taken_positions_by_letter, wrong_place_letters=[], forbidden_letters=set()):
    already_taken_positions_by_letter = copy.deepcopy(already_taken_positions_by_letter)
    # Keep the words with the wrongly placed letters
    for letter_and_wrong_position in wrong_place_letters:
        letter = list(letter_and_wrong_position)[0]
        wrong_position = letter_and_wrong_position[letter]

        possible_position = detect_possible_possible_position_for_wrong_place_letter(word, already_taken_positions_by_letter, letter, wrong_position)
        if possible_position > 0:
            already_taken_positions_by_letter[letter].append(possible_position)
        else:
            return False

    # When we discard the letters already used in word, the word should not contain any forbidden_letter
    already_taken_positions = []
    for letter, positions in already_taken_positions_by_letter.items():
        already_taken_positions.extend(positions)

    word_without_discarded_letters = [word_letter for word_letter, letter_position in zip(word, range(0, len(word)))
                                     if letter_position+1 not in already_taken_positions]

    for forbidden_letter in forbidden_letters:
        if forbidden_letter in word_without_discarded_letters:
            return False

    return True


def get_possible_words(words, word_len, known_letters=[], wrong_place_letters=[], forbidden_letters=set()):
    possible_words = keep_words_with_len(words, word_len)

    # Keeps track of the letter already placed
    already_taken_positions_by_letter = {letter: [] for letter in list(string.ascii_uppercase)}

    # Keep only the words with the known letters in the right place
    for letter_and_position in known_letters:
        letter = list(letter_and_position)[0]
        position = letter_and_position[letter]

        already_taken_positions_by_letter[letter].append(position)
        possible_words = keep_words_with_known_letter(possible_words, letter, position)

    if len(possible_words) == 0:
        raise Exception(f"There is no word of size '{word_len}' with known letters '{known_letters}' in the dictionary")

    possible_words_with_wrong_place_letters = [word for word in possible_words if
                                               is_word_possible(word, already_taken_positions_by_letter,
                                                                wrong_place_letters, forbidden_letters)]

    return possible_words_with_wrong_place_letters

def get_proba_for_letter(word, letter):
    nb_occurences = sum(word_letter == letter for word_letter in word)
    proba = 0.0
    if nb_occurences > 0:
        proba = 1.0 * (0.66 ** (nb_occurences-1))
    return proba


def get_best_word_from_possibilities(words):
    # For the moment, simple way: hard-coding a preference for 'T', 'R', and 'E' and decrease each by 33% each time they reappear
    word_probas = {}
    for word in words:
        proba_t = get_proba_for_letter(word, 'T')
        proba_r = get_proba_for_letter(word, 'R')
        proba_e = get_proba_for_letter(word, 'E')

        word_probas[word] = (proba_t + proba_r + proba_e) / 3

    word_probas_ranked = sorted(word_probas.items(), key=lambda x: x[1], reverse=True)
    result = word_probas_ranked[0][0]
    return result

def get_correct_letters(word, word_to_guess):
    correct_letters = []
    for letter_word, letter_word_to_guess, position in zip(word, word_to_guess, range(0, len(word))):
        if letter_word == letter_word_to_guess:
            correct_letters.append({letter_word: position+1})
    return correct_letters

def get_wrong_place_and_forbidden_letters(word, word_to_guess, correct_letters):
    word_letters = list(word)
    word_to_guess_letters = list(word_to_guess)
    # In order to ease our life, we replace the letters which are already correct by - in both words, in order to tag
    # them as 'already taken'
    for letter_and_position in correct_letters:
        letter = list(letter_and_position)[0]
        position = letter_and_position[letter]-1
        word_letters[position] = '-'
        word_to_guess_letters[position] = '-'

    wrong_place_letters = []
    for letter_word, letter_word_to_guess, position in zip(word_letters, word_to_guess_letters, range(0, len(word_letters))):
        if letter_word != letter_word_to_guess and letter_word in word_to_guess_letters:
            wrong_place_letters.append({letter_word: position+1})
            word_letters[position] = '-'
            # Find the first occurrence of the letter in the word to guess and replace it by '-'
            for letter_in_word_guess, position_letter_in_word_to_guess in zip(word_to_guess_letters, range(0, len(word_to_guess_letters))):
                if letter_in_word_guess == letter_word:
                    word_to_guess_letters[position_letter_in_word_to_guess] = '-'
                    break

    # The forbidden letters have not been tagged in the attempted word
    forbidden_letters = set([letter for letter in word_letters if letter != '-'])
    return wrong_place_letters, forbidden_letters

def run_sutom(word_to_guess):
    possible_words = read_file_dict()
    known_letters = [{word_to_guess[0]: 1}]
    wrong_place_letters = []
    forbidden_letters = set()

    attempts = []

    while True:
        possible_words = get_possible_words(possible_words, len(word_to_guess), known_letters=known_letters,
                                            wrong_place_letters=wrong_place_letters,
                                            forbidden_letters=forbidden_letters)
        best_word = get_best_word_from_possibilities(possible_words)
        attempts.append(best_word)

        correct_letters = get_correct_letters(best_word, word_to_guess)
        wrong_place_letters, new_forbidden_letters = get_wrong_place_and_forbidden_letters(best_word, word_to_guess, correct_letters)
        forbidden_letters.update(new_forbidden_letters)

        if best_word == word_to_guess:
            break

    return attempts

def run_challenge(words_to_guess):
    result = [len(run_sutom(word_to_guess)) for word_to_guess in words_to_guess]
    return result

if __name__ == '__main__':
    words = read_file_dict()
    possible_words = get_possible_words(words, 7, known_letters=[{'S': 1}, {'R': 3}, {'T': 6}, {'E': 7}], wrong_place_letters=[{'I': 4}], forbidden_letters={'A', 'B', 'O', 'C', 'P'})
    best_word = get_best_word_from_possibilities(possible_words)
    print(best_word)

