import string
import copy
import numpy as np


def read_file(filename='pli07.txt'):
    with open(filename) as file:
        words = [line.rstrip() for line in file]

    return words


def keep_words_with_length(words, word_len):
    words = [word for word in words if len(word) == word_len]

    if len(words) == 0:
        raise Exception(f"There is no word with size '{word_len}' in the dictionary")

    return words


def _detect_possible_position_for_wrong_place_letter(word, already_taken_positions_by_letter, letter,
                                                     wrong_position):
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


def _is_word_possible(word, already_taken_positions_by_letter, wrong_place_letters=[], forbidden_letters=set()):
    """
    This function is called by get_possible_words() below. It returns True if 'word' is allowed by the rules:
    - 'word' must contain the wrong placed letters, but in another position. These letters should not have been already
        'taken' by the correctly placed letters, ie. they must not be in 'already_taken_positions_by_letter'
    - 'word' must not contain any of the forbidden letters

    Note: this function is able to deal with tricky situations. For example, the word can contain 'E' at position 1,
    it can also contain 'E' at a position different from '3', and we might be sure that there is no other 'E'. In that
    example: 'already_taken_positions_by_letter' would indicate that 'E' is already taken at position 1,
    'wrong_place_letters' would contain 'E' at position 3 (because the searched word should contain a second 'E', but
    not at position 3), and 'forbidden_letters' would contain 'E', because there is no other 'E' in the searched word.

    :param word: the word that we want to check
    :param already_taken_positions_by_letter: dict{ letter, list of positions_taken_by_this_letter }
    :param wrong_place_letters:
    :param forbidden_letters:
    :return:
    """
    already_taken_positions_by_letter = copy.deepcopy(already_taken_positions_by_letter)
    # Keep the words with the wrongly placed letters
    for letter, wrong_position in wrong_place_letters:
        possible_position = _detect_possible_position_for_wrong_place_letter(word,
                                                                             already_taken_positions_by_letter,
                                                                             letter, wrong_position)
        if possible_position > 0:
            already_taken_positions_by_letter[letter].append(possible_position)
        else:
            return False

    # When we discard the letters already used in word, the word should not contain any forbidden_letter
    already_taken_positions = []
    for letter, positions in already_taken_positions_by_letter.items():
        already_taken_positions.extend(positions)

    word_without_discarded_letters = [word_letter for word_letter, letter_position in zip(word, range(0, len(word)))
                                      if letter_position + 1 not in already_taken_positions]

    for forbidden_letter in forbidden_letters:
        if forbidden_letter in word_without_discarded_letters:
            return False

    return True


def get_possible_words(words, known_letters=[], wrong_place_letters=[], forbidden_letters=set()):
    """
    Returns the 'possible' words from the list 'words': they must contain the known
    letters at the right place, they must contain the wrong placed letter at some other place, and they must not
    contain the forbidden letters

    :param words: list of words to be filtered by this function
    :param known_letters: list of tuples, such as [('T', 1), ('E', 3)]. In this example, the expected words must contain
    T at position 1 and E at position 3.
    :param wrong_place_letters: list of tuples, such as [('A', 2), ('K', 4)]. In this example, the expected words must
    contain A, but not at position 2, and K, but not at position 4.
    :param forbidden_letters: list of letters. The expected words must not contain any of these letters.
    :return: A list of words filtered by the rules above.
    """

    def _does_word_contain_known_letter(word, letter, position):
        if position > len(word):
            # Sanity check: the position of the letter should not be bigger than the size of the word (!!)
            raise Exception(f"Position '{position}' of letter '{letter}' is bigger than the word size '{len(word)}'")

        return word[position - 1] == letter

    # Keeps track of the letter already placed
    already_taken_positions_by_letter = {letter: [] for letter in list(string.ascii_uppercase)}

    # Keep only the words with the known letters in the right place
    for letter, position in known_letters:
        already_taken_positions_by_letter[letter].append(position)
        words = [word for word in words if _does_word_contain_known_letter(word, letter, position)]

    if len(words) == 0:
        raise Exception(f"There is no word with known letters '{known_letters}' in the dictionary")

    possible_words_with_wrong_place_letters = [word for word in words if
                                               _is_word_possible(word, already_taken_positions_by_letter,
                                                                 wrong_place_letters, forbidden_letters)]

    return possible_words_with_wrong_place_letters


def preference_for_letters_TRE(words):
    """
    Returns the best candidate for the next attempt, from the list 'words'
    :param words: list of words
    :return: best candidate
    """

    def _get_proba_for_letter(word, letter):
        nb_occurrences = sum(word_letter == letter for word_letter in word)
        proba = 0.0
        if nb_occurrences > 0:
            proba = 1.0 * (0.66 ** (nb_occurrences - 1))
        return proba

    # For the moment, simple way: hard-coding a preference for 'T', 'R', and 'E' and decrease each by 33% each time
    # they reappear
    word_probas = {}
    for word in words:
        proba_t = _get_proba_for_letter(word, 'T')
        proba_r = _get_proba_for_letter(word, 'R')
        proba_e = _get_proba_for_letter(word, 'E')

        word_probas[word] = (proba_t + proba_r + proba_e) / 3

    word_probas_ranked = sorted(word_probas.items(), key=lambda x: x[1], reverse=True)
    result = word_probas_ranked[0][0]
    return result


def statistically_optimal_word(words):
    """
    It sounds like an evidence, but this is exactly the principle of this function: if we chose the best word, we get
    the smallest number of possible words afterwards
    => for each word, we have to imagine that it is the correct word (ie. the word to guess), and check how many
    possible words we would get if we chose any other word from 'words'
    => the best word is the one with the smallest result

    :param words:
    :return:
    """

    def get_score(essai, solution):
        known_letters = _get_correct_letters(essai, solution)
        wrong_place_letters, forbidden_letters = _get_wrong_place_and_forbidden_letters(essai,
                                                                                        solution,
                                                                                        known_letters)
        possible_words = get_possible_words(words, known_letters=known_letters,
                                            wrong_place_letters=wrong_place_letters,
                                            forbidden_letters=forbidden_letters)
        return len(possible_words)

    def get_score_for_solution(solution):
        scores_solution = [get_score(essai, solution) for essai in words]
        score = np.sum(scores_solution)
        return score

    scores = [get_score_for_solution(solution) for solution in words]

    result = words[np.argmin(scores)]
    return result

def _get_correct_letters(word, word_to_guess):
    correct_letters = []
    for letter_word, letter_word_to_guess, position in zip(word, word_to_guess, range(0, len(word))):
        if letter_word == letter_word_to_guess:
            correct_letters.append((letter_word, position + 1))
    return correct_letters


def _get_wrong_place_and_forbidden_letters(word, word_to_guess, correct_letters):
    word_letters = list(word)
    word_to_guess_letters = list(word_to_guess)
    # In order to ease our life, we replace the letters which are already correct by - in both words, in order to tag
    # them as 'already taken'
    for letter, position in correct_letters:
        word_letters[position - 1] = '-'
        word_to_guess_letters[position - 1] = '-'

    wrong_place_letters = []
    for letter_word, letter_word_to_guess, position in zip(word_letters, word_to_guess_letters,
                                                           range(0, len(word_letters))):
        if letter_word != letter_word_to_guess and letter_word in word_to_guess_letters:
            wrong_place_letters.append((letter_word, position + 1))
            word_letters[position] = '-'
            # Find the first occurrence of the letter in the word to guess and replace it by '-'
            for letter_in_word_guess, position_letter_in_word_to_guess in zip(word_to_guess_letters,
                                                                              range(0, len(word_to_guess_letters))):
                if letter_in_word_guess == letter_word:
                    word_to_guess_letters[position_letter_in_word_to_guess] = '-'
                    break

    # The forbidden letters have not been tagged in the attempted word
    forbidden_letters = set([letter for letter in word_letters if letter != '-'])
    return wrong_place_letters, forbidden_letters


def _run_sutom(word_to_guess, possible_words, candidate_selector):
    known_letters = [(word_to_guess[0], 1)]
    wrong_place_letters = []
    forbidden_letters = set()

    attempts = []

    while True:
        possible_words = get_possible_words(possible_words, known_letters=known_letters,
                                            wrong_place_letters=wrong_place_letters,
                                            forbidden_letters=forbidden_letters)

        # Sanity check: the word to guess could not be found if possible_words is empty
        if len(possible_words) == 0:
            raise Exception(f"The word {word_to_guess} could not be guessed.")

        best_word = candidate_selector(possible_words)
        attempts.append(best_word)

        known_letters = _get_correct_letters(best_word, word_to_guess)
        wrong_place_letters, new_forbidden_letters = _get_wrong_place_and_forbidden_letters(best_word, word_to_guess,
                                                                                            known_letters)
        forbidden_letters.update(new_forbidden_letters)

        if best_word == word_to_guess:
            break

    return attempts


def run_sutom(word_to_guess, candidate_selector=preference_for_letters_TRE):
    possible_words = read_file()
    possible_words = keep_words_with_length(possible_words, len(word_to_guess))
    result = _run_sutom(word_to_guess, possible_words, candidate_selector)
    return result


def run_challenge(words_to_guess, candidate_selector=preference_for_letters_TRE):
    possible_words = read_file()
    result = [
        len(_run_sutom(word_to_guess, keep_words_with_length(possible_words, len(word_to_guess)), candidate_selector))
        for word_to_guess in words_to_guess]
    return result


if __name__ == '__main__':
    words = read_file()
    words = keep_words_with_length(words, 7)
    words = get_possible_words(words, known_letters=[('S', 1), ('R', 3), ('T', 6), ('E', 7)],
                               wrong_place_letters=[('I', 4)], forbidden_letters={'A', 'B', 'O', 'C', 'P'})
    best_word = preference_for_letters_TRE(words)
    print(best_word)
