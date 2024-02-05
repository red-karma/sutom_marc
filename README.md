# SUTOM Solver
See the game at https://sutom.nocle.fr/#

# How to crack the SUTOM of the day
Let's say that the word of the day starts with "S" and contains 7 letters. The SUTOM game would show this grid:

![img.png](img.png)

In order to crack it, please call the following functions:

    # Read the dictionary pli07.txt
    words = read_file_dict()
    # Get the words starting with 'S' and containing 7 letters
    words = main.keep_words_with_length(words, 7)
    possible_words = get_possible_words(words, known_letters=[('S', 1)])
    # From this list, get the most probable word
    best_word = get_best_word_from_possibilities(possible_words)

Let's imagine that the solver outputs the word SABOTER. Please type it the game SUTOM. Let's imagine that the game gives this result:

![img_1.png](img_1.png)

The red letters are in the word to guess, at that place. The orange letters are in the word to guess, but at the wrong place. The blue ones are not in the word to guess. It means that you have to call the solver with the following parameters:


    # Read the dictionary pli07.txt
    words = read_file_dict()
    words = main.keep_words_with_length(words, 7)
    possible_words = get_possible_words(words, known_letters=[('S': 1)], wrong_place_letters=[('T', 5), ('E', 6), ('R', 7)], forbidden_letters={'A', 'B', 'O'})
    # From this list, get the most probable word
    best_word = get_best_word_from_possibilities(possible_words)

Now, let's imagine that the solver outputs SCRIPTE. Again, you type that word in the game SUTOM. Let's imagine that the game outputs this result:

![img_2.png](img_2.png)

I presume that you see the idea: you have to call the solver with this new result. Just don't forget to put all the forbidden letters:

    words = read_file_dict()
    words = main.keep_words_with_length(words, 7)
    possible_words = get_possible_words(words, known_letters=[('S', 1), ('R', 3), ('T', 6), ('E', 7)], wrong_place_letters=[('I', 4)], forbidden_letters={'A', 'B', 'O', 'C', 'P'})
    best_word = get_best_word_from_possibilities(possible_words)

Now the solver outputs SURDITE, and you win:

![img_3.png](img_3.png)

# If you want to improve the solver

The quality of the solver relies on 2 things:
- The quality of the dictionary pli07.txt
- The quality of the best possible word found by the function get_best_word_from_possibilities()

Therefore, you can try to improve it - for the moment, it is very simple.
In order to evaluate the quality of the function get_best_word_from_possibilities(), you can let the solver work alone and compete against other solvers.

In order to do so, you can call the function run_sutom(word_to_guess). It returns the number of attempts of the solver before finding your word.
For example:

        attempts = run_sutom('SURDITE')

returns ['SABOTER', 'SCRIPTE', 'SURDITE']. It means that it found 'SURDITE' in 3 attempts.

You can also call run_challenge on a list of words to guess, in order to evaluate your solver on several words. Example:

        nb_attempts = main.run_challenge(['SURDITE', 'SCRUPULE', 'ECOEURE'])

Returns [3, 3, 3]: the solver found 'SURDITE' in 3 attemps, 'SCRUPULE' in 3 attempts, and 'ECOEURE' in 3 attempts.