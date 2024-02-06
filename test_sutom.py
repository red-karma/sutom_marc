import unittest

import main

class MyTestCase(unittest.TestCase):
    def test_get_possible_words_size_10_start_with_Z(self):
        words = main.read_file()
        words = main.keep_words_with_length(words, 10)
        possible_words = main.get_possible_words(words, known_letters=[('Z', 1)])
        self.assertListEqual(possible_words, ['ZEZAIEMENT', 'ZIDOVUDINE', 'ZIGOUILLER', 'ZIGZAGUANT', 'ZIMBABWEEN', 'ZOANTHAIRE', 'ZOOLOGISTE', 'ZOOTECHNIE', 'ZOZOTEMENT', 'ZURICHOISE', 'ZYGOMORPHE', 'ZYGOMYCETE', 'ZYGOPETALE'])  # add assertion here

    def test_get_possible_words_size_8_start_with_Z_with_known_letters(self):
        words = main.read_file()
        words = main.keep_words_with_length(words, 8)
        possible_words = main.get_possible_words(words, known_letters=[('Z', 1), ('A', 2)])
        self.assertListEqual(possible_words, ['ZAIBATSU', 'ZAIROISE', 'ZAKOUSKI', 'ZANZIBAR', 'ZAPPETTE', 'ZAPPEUSE', 'ZARZUELA'])

    def test_get_possible_words_size_8_start_with_Z_with_wrong_letters(self):
        words = main.read_file()
        words = main.keep_words_with_length(words, 8)
        possible_words = main.get_possible_words(words, known_letters=[('Z', 1), ('A', 2)], wrong_place_letters=[('I', 3)])
        self.assertListEqual(possible_words, ['ZAKOUSKI', 'ZANZIBAR'])

    def test_get_possible_words_size_8_start_with_Z_with_wrong_letters_and_forbidden(self):
        words = main.read_file()
        words = main.keep_words_with_length(words, 8)
        possible_words = main.get_possible_words(words, known_letters=[('Z', 1), ('A', 2)], wrong_place_letters=[('I', 5)], forbidden_letters=['I'])
        # Not ZANZIBAR because I would be correct in position 5
        # Not ZAIROISE because the second I is forbidden
        self.assertListEqual(possible_words, ['ZAIBATSU', 'ZAKOUSKI'])

    def test_best_word(self):
        words = main.read_file()
        words = main.keep_words_with_length(words, 8)
        possible_words = main.get_possible_words(words, known_letters=[('A', 1)])
        best_word = main.preference_for_letters_TRE(possible_words)
        self.assertEqual(best_word, 'ABORTIVE')

    def test_run_sutom(self):
        attempts = main.run_sutom('SURDITE')
        self.assertListEqual(attempts, ['SABOTER', 'SCRIPTE', 'SURDITE'])

    def test_run_sutom_2(self):
        attempts = main.run_sutom('SCRUPULE')
        self.assertListEqual(attempts, ['SABOTEUR', 'SCISSURE', 'SCRUPULE'])

    def test_run_sutom_3(self):
        attempts = main.run_sutom('ECOEURE')
        self.assertListEqual(attempts, ['ECRIANT', 'ECHOUER', 'ECOEURE'])

    def test_run_sutom_with_candidate_selector(self):
        def first_word_in_list(words):
            return words[0]

        attempts = main.run_sutom('SURDITE', candidate_selector=first_word_in_list)
        self.assertListEqual(attempts, ['SABAYON', 'SCELLER', 'SPIRITE', 'SURDITE'])

    def test_run_sutom_with_statistically_optimal_candidate_selector(self):

        attempts = main.run_sutom('SURDITE', candidate_selector=main.statistically_optimal_word)
        self.assertListEqual(attempts, ['SAUTOIR', 'STRIURE', 'SURDITE'])

    def test_run_challenge(self):
        nb_attempts = main.run_challenge(['SURDITE', 'SCRUPULE', 'ECOEURE'])
        self.assertListEqual(nb_attempts, [3, 3, 3])

    def test_run_challenge_with_candidate_selector(self):
        def first_word_in_list(words):
            return words[0]

        nb_attempts = main.run_challenge(['SURDITE', 'SCRUPULE', 'ECOEURE'], candidate_selector=first_word_in_list)
        self.assertListEqual(nb_attempts, [4, 4, 2])

if __name__ == '__main__':
    unittest.main()
