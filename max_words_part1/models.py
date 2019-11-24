import argparse
from multiprocessing import Pool
from io import DEFAULT_BUFFER_SIZE
import re

import pygtrie as tri

from word_counter_part1 import utils


class Parser:
    def __init__(self):
        parser = self.setup_parser()
        self.args = parser.parse_args()
        self.validate_args()

    def setup_parser(self):
        parser = argparse.ArgumentParser(description='Count maximum N words in a specific path')
        parser.add_argument(dest='max_num', help='number of the most shown words in the files')
        parser.add_argument(dest='paths', nargs='*', help='path for a folder/file')
        return parser

    def validate_args(self):
        if not self.args.max_num.isdigit():
            print('Error - please enter a number for the first parameter')


class WordCounter:
    def __init__(self, args):
        self.paths = args.paths
        self.max_num = int(args.max_num)
        self.final_trie = tri.Trie()
        self.trie_per_file = []
        self.__char_to_remove = re.compile('[,.!?*#();:\[\]{}]')
        self.count_words()


    def _read_file(self, path):
        """
        :param path: path of a file
        :return: Trie object with all counted word
        """
        trie = tri.Trie()
        with open(path, 'r', buffering=DEFAULT_BUFFER_SIZE) as f:
            for line in f:
                for word in line.split():
                    word = self.__char_to_remove.sub('', word.lower())
                    if word in trie:
                        trie[word] += 1
                    else:
                        trie[word] = 1
        return trie

    def count_words(self):
        text_files = utils.get_text_files_from_paths(self.paths)
        with Pool(processes=4) as pool:
            self.trie_per_file = pool.map(self._read_file, text_files)
        self._create_summary()
        top_n = utils.get_top_n_frequent(self.final_trie, self.max_num)
        self.print_summary(top_n)

    def print_summary(self, top_n):
        print(f'Maximum​ {self.max_num}​​ words:')
        for max_value in top_n:
            word = ''.join(max_value[1])
            print(f'Word \'{word}\' occurred {-max_value[0]}')

    def _create_summary(self):
        for file in self.trie_per_file:
            for word in file:
                if word in self.final_trie:
                    self.final_trie[word] += file[word]
                else:
                    self.final_trie[word] = file[word]
