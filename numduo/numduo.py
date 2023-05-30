import argparse
import glob
import logging
import os

from typing import List, Tuple
from settings.settings import LOG_SCRIPT_PATH
from utils.decorators import log_decorator


class NumDuo:
    """A class for finding all unique pairs of numbers in a given list of integers.

    Attributes:
    -----------
    data : List[int]
        A list of integers.
    pairs : List[List[int, int]]
        A list of tuples representing all unique pairs of integers in the data list.

    Methods:
    --------
      Methods:
        __init__(self, data: List[int]) -> None:
            Initializes the NumDuo object with a given list of integers.

        find_pairs(self) -> List[List[int]]:
            Finds all unique pairs of integers in the data list that add up to 12 and stores them in pairs attribute.
            Returns a list of pairs of integers, where each pair is represented as a list of two integers.

        get_pairs(self) -> List[int, int]:
            Gets pairs of numbers from `self.data` that add up to 12.
            Prints the string representation of each pair to stdout.
            Returns all pairs as a tuple, where the first element is a list of pairs of numbers (represented as tuples),
            and the second element is always `None`.

        _validate_input_file() -> None:
            This is a static method.
            Raise a ValueError if an input file path does not have a '.txt' extension.

        _validate_positive_number() -> None:
            This is a static method.
            Checks if all the numbers in the list are positive.

        from_input_file(cls, input_file: str) -> 'NumDuo':
            Creates a new instance of `NumDuo` by reading data from an input file.
            The input file should have the following format: [num1,num2,...,numN] where each number is an integer.

        to_output_file(self, output_file: str) -> None:
            Writes the pairs of numbers from `self.pairs` to an output file.
            Each pair is written as a string in the format "num1 num2", followed by a newline character.

        main(cls) -> None:
            The entry point for this script.
            Parses command line arguments and runs the algorithm to find pairs of numbers that add up to 12.
            Writes the output to a file and logs any errors or warnings to the console and to a log file.
    """

    def __init__(self, data: List[int]) -> None:
        """
        Initializes the NumDuo object with a given list of integers.

        Parameters:
        -----------
        data : List[int]
            A list of integers.
        """
        self.data = data
        self.pairs = []

    @log_decorator
    def find_pairs(self) -> List[List[int]]:

        """
        Find pairs of numbers in `self.data` that add up to 12.
        Only add pairs that are unique and have not yet been added.
        Return a list of pairs of numbers, where each pair is represented as a list of two integers.

        Returns:
            List[List[int]]: A list of pairs of numbers, where each pair is represented as a list of two integers.
        """

        used = []

        for i, num1 in enumerate(self.data):
            if num1 in used or num1 > 12:
                continue
            for num2 in self.data[i + 1:]:
                if num1 + num2 == 12 and [num1, num2] not in used:
                    if num1 <= num2:
                        self.pairs.append([num1, num2])
                    else:
                        self.pairs.append([num2, num1])
                    used.append([num1, num2])
        return self.pairs

    def get_pairs(self) -> List:
        """
        Get pairs of numbers from `self.data` that add up to 12.
        Print the string representation of each pair to stdout.
        Return all pairs as a tuple, where the first element is a list of pairs of numbers (represented as tuples),
        and the second element is always `None`.

        Returns:
            List[List[int]]: A tuple containing a list of pairs of numbers and None.
        """
        self.find_pairs()

        pairs_str = "\n".join([f"{pair[0]} {pair[1]}" for pair in self.pairs])
        print(pairs_str)

        return self.pairs

    @staticmethod
    def _validate_input_file(input_file: str) -> None:
        """Raise a ValueError if an input file path does not have a '.txt' extension.

        Args:
            input_file(str): A path to an input file.

        Raises:
            ValueError: If an input file path does not have a '.txt' extension.
        """

        if not input_file.endswith('.txt'):
            raise ValueError("Input file must be a .txt file.")

    @staticmethod
    def _validate_positive_numbers(data: List[int]) -> None:
        """
        Checks if all the numbers in the list are positive.

        Args:
            data (List[int]): The list of numbers to validate.

        Raises:
            ValueError: If any number in the list is non-positive.
        """
        if any(num < 0 for num in data):
            raise ValueError("Input file contains non-positive numbers.")

    @classmethod
    def from_input_file(cls, input_file: str) -> 'NumDuo':
        """
        Create a new instance of `NumDuo` by reading data from an input file.
        The input file should have the following format:
        [num1,num2,...,numN]
        where each number is an integer.

        Args:
            cls (type): The class calling this method.
            input_file (str): The path to the input file.

        Raises:
            ValueError: If the input file does not exist or has an unsupported extension.

        Returns:
            NumDuo: A new instance of `NumDuo`.
        """
        try:
            NumDuo._validate_input_file(input_file)
            with open(input_file, 'r') as f:
                data_str = f.readline().strip().replace("[", "").replace("]", "")
                data = [int(x) for x in data_str.split(",")]
                NumDuo._validate_positive_numbers(data)
            return cls(data)
        except FileNotFoundError as e:
            raise ValueError(f"Input file {input_file} not found.") from e

    def to_output_file(self, output_file: str) -> None:
        """
        Write the pairs of numbers from `self.pairs` to an output file.
        Each pair is written as a string in the format "num1 num2", followed by a newline character.

        Args:
            self (NumDuo): The `NumDuo` instance.
            output_file (str): The path to the output file.

        Returns:
            None
        """
        with open(output_file, 'w') as f:
            for pair in self.pairs:
                f.write(f"{pair[0]} {pair[1]}\n")

    @classmethod
    def main(cls) -> None:
        """
        The entry point for this script.
        Parses command line arguments and runs the algorithm to find pairs of numbers that add up to 12.
        Writes the output to a file and logs any errors or warnings to the console and to a log file.

        Returns:
            None
        """

        logging.basicConfig(filename=f'{LOG_SCRIPT_PATH}', level=logging.INFO,
                            format='%(asctime)s %(levelname)s %(message)s')

        # Add command line arguments
        parser = argparse.ArgumentParser(description='Find number pairs from data')
        parser.add_argument('--input-dir', type=str, default='data/input/',
                            help='directory containing input files')
        parser.add_argument('--input-files', type=str, nargs='+', default=None,
                            help='list of paths to input files (overrides --input-dir)')
        parser.add_argument('--output-dir', type=str, default='data/output/',
                            help='path to output directory')

        args = parser.parse_args()

        if args.input_files is None:
            # Find all .txt files in the input directory
            input_files = [os.path.normpath(file) for file in glob.glob(f'{args.input_dir}/*.txt')]
        else:
            # Use the provided list of input files
            input_files = args.input_files

        output_dir = args.output_dir

        for input_file in input_files:
            logging.info(f'Reading input from file {input_file}.')
            numduo = NumDuo.from_input_file(input_file)

            try:
                result = numduo.get_pairs()
                logging.info(f"Found {len(result)} pairs.")
                output_file = os.path.join(
                    output_dir,
                    f'output_of_{os.path.splitext(os.path.basename(input_file))[0]}.txt',
                )
                numduo.to_output_file(output_file)
                print(f'Result for {input_file} written to file {output_file}.')
            except Exception as e:
                logging.error(f"An error occurred: {str(e)}.")
