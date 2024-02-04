import unittest

import main

class MyTestCase(unittest.TestCase):
    def test_get_possible_words_size_10_start_with_Z(self):
        words = main.read_file_dict()
        possible_words = main.get_possible_words(words, 10, known_letters=[{'Z': 1}])
        self.assertListEqual(possible_words, ['ZEZAIEMENT', 'ZIDOVUDINE', 'ZIGOUILLER', 'ZIGZAGUANT', 'ZIMBABWEEN', 'ZOANTHAIRE', 'ZOOLOGISTE', 'ZOOTECHNIE', 'ZOZOTEMENT', 'ZURICHOISE', 'ZYGOMORPHE', 'ZYGOMYCETE', 'ZYGOPETALE'])  # add assertion here

    def test_get_possible_words_size_8_start_with_Z_with_known_letters(self):
        words = main.read_file_dict()
        possible_words = main.get_possible_words(words, 8, known_letters=[{'Z': 1}, {'A': 2}])
        self.assertListEqual(possible_words, ['ZAIBATSU', 'ZAIROISE', 'ZAKOUSKI', 'ZANZIBAR', 'ZAPPETTE', 'ZAPPEUSE', 'ZARZUELA'])

    def test_get_possible_words_size_8_start_with_Z_with_wrong_letters(self):
        words = main.read_file_dict()
        possible_words = main.get_possible_words(words, 8, known_letters=[{'Z': 1}, {'A': 2}], wrong_place_letters=[{'I': 3}])
        self.assertListEqual(possible_words, ['ZAKOUSKI', 'ZANZIBAR'])

    def test_get_possible_words_size_8_start_with_Z_with_wrong_letters_and_forbidden(self):
        words = main.read_file_dict()
        possible_words = main.get_possible_words(words, 8, known_letters=[{'Z': 1}, {'A': 2}], wrong_place_letters=[{'I': 5}], forbidden_letters=['I'])
        # Not ZANZIBAR because I would be correct in position 5
        # Not ZAIROISE because the second I is forbidden
        self.assertListEqual(possible_words, ['ZAIBATSU', 'ZAKOUSKI'])

    def test_best_word(self):
        words = main.read_file_dict()
        possible_words = main.get_possible_words(words, 8, known_letters=[{'A': 1}])
        best_word = main.get_best_word_from_possibilities(possible_words)
        self.assertEqual(best_word, 'ABORTIVE')

    def test_run_sutom(self):
        attempts = main.run_sutom('SURDITE')
        self.assertListEqual(attempts, ['SABOTER', 'SCRIPTE', 'SURDITE'])

    def test_run_challenge(self):
        nb_attempts = main.run_challenge(['SURDITE', 'SCRUPULE', 'ECOEURE'])
        self.assertListEqual(nb_attempts, [3, 3, 4])

if __name__ == '__main__':
    unittest.main()
