import unittest

from mock import mock_open, patch, call
from numduo.numduo import NumDuo


class TestNumDuo(unittest.TestCase):
    def setUp(self):
        self.nd = NumDuo([4, 8, 9, 0, 12, 1, 4, 2, 12, 12, 4, 4, 8, 11, 12, 0, 6])
        self.test_data = [1, 2, 3, 4, 5, 8, 9]
        self.test_cases = [
            {
                "data": [1, 2, 3, 4, 9],
                "expected_output": [[3, 9]],
            },
            {
                "data": [6, 6, 3, 9, 4, 8, 1, 11],
                "expected_output": [[6, 6], [3, 9], [4, 8], [1, 11]],
            },
            {
                "data": [2, 6, 4, 7, 5],
                "expected_output": [[5, 7]],
            },
        ]

    def test_create_numduo_instance(self):
        self.assertEqual([4, 8, 9, 0, 12, 1, 4, 2, 12, 12, 4, 4, 8, 11, 12, 0, 6], self.nd.data)
        self.assertIsInstance(self.nd.data, list)

    def test_find_pairs(self):
        for case in self.test_cases:
            data = case["data"]
            expected_output = case["expected_output"]
            nd = NumDuo(data)

            self.assertListEqual(nd.find_pairs(), expected_output)

    def test_get_pairs(self):
        pairs = self.nd.get_pairs()
        self.assertEqual(len(pairs), 5)
        self.assertIn([4, 8], pairs)
        self.assertNotIn([8, 4], pairs)
        self.assertNotIn([6, 6], pairs)

    def test_validate_input_file_with_txt_file(self):
        input_file = "test.txt"
        nd = self.nd

        self.assertIsNone(nd._validate_input_file(input_file))

    def test_validate_input_file_with_non_txt_file(self):
        input_file = "test.csv"
        nd = self.nd

        # Act & Assert
        with self.assertRaises(ValueError):
            nd._validate_input_file(input_file)

    @patch('builtins.open', new_callable=mock_open, read_data='[2, 4, 6, 8]')
    def test_from_input_file(self, mock_file):
        nd = NumDuo.from_input_file('test.txt')
        self.assertEqual(nd.data, [2, 4, 6, 8])

    @patch('builtins.open', new_callable=mock_open)
    def test_to_output_file(self, mock_file):
        nd = NumDuo([2, 4, 6, 8])
        nd.pairs = [(2, 4), (6, 8)]
        nd.to_output_file('test_output.txt')
        mock_file.assert_called_with('test_output.txt', 'w')
        handle = mock_file()
        handle.write.assert_has_calls([call('2 4\n'), call('6 8\n')])

    @patch('numduo.numduo.NumDuo.main')
    def test_main_called(self, mock_main):
        NumDuo.main()
        mock_main.assert_called_once()

    def tearDown(self):
        del self.nd


if __name__ == '__main__':
    unittest.main()
