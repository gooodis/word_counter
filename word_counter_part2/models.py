#!/usr/bin/python
import argparse
from multiprocessing import Pool
import os
from io import DEFAULT_BUFFER_SIZE
import re

import datefinder
import pygtrie as tri

from word_counter_part2 import utils

TEXT_FILES_SUFFIXES = {'txt', 'log'}
LOGS_FOLDER_PATH = '/var/log'
DATE_PATTERN = "%b %d %H:%M:%S"
CLOCK_PATTERN = '[0-2][0-9]:[0-5][0-9]:[0-5][0-9]'


class Parser:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Count maximum N words in a specific path')
        parser.add_argument(dest='max_num', help='number of the most shown words in the files')
        parser.add_argument(dest='time_frames', nargs='*', help='time frame examination')
        parser.add_argument('--debug', default=True, dest='debug', help='print examined log file names')
        self.args = parser.parse_args()
        self.args.time_frames = self.parse_time_frames()
        self.validate_args()

    def parse_time_frames(self):
        modified_tf = []
        if self.args.time_frames[0].isdigit():
            for chunk in utils.get_chunks(self.args.time_frames, 3):
                if re.search(r'[0-9]+-[0-9]+', ''.join(chunk)):
                    re.compile('[,]')
                    modified_tf.append([int(re.compile('[,]').sub('', chunk[0])),
                                        int(re.compile('[,]').sub('', chunk[2]))])
        else:
            time_frames = self.parse_date_string(self.args.time_frames)
            for tf in time_frames:
                modified_tf.append([utils.parse_date(tf[0]).timestamp(), utils.parse_date(tf[1]).timestamp()])
        return modified_tf

    def validate_args(self):
        if not self.args.max_num.isdigit():
            print('Error - please enter a number for the first parameter')
        for chunk in self.args.time_frames:
            if chunk[0] > chunk[1]:
                print('Error - please enter a legal time frame')

    def parse_date_string(self, time_frames):
        retval = []
        tmp_list = []
        for word in time_frames:
            if word == '-':
                continue
            tmp_list.append(word)
            if re.search(CLOCK_PATTERN, word):
                retval.append(' '.join(tmp_list))
                tmp_list = []
        return utils.get_chunks(retval, 2)


class WordCounter:
    def __init__(self, args):
        print(args.time_frames)
        self._time_frames = utils.merge_intervals(args.time_frames)
        self._max_num = int(args.max_num)
        self.final_trie = tri.Trie()
        self.__trie_per_file = []
        self.__char_to_remove = re.compile('[=,.!?*#();:\[\]{}]')
        self._counted_word_files = set()
        self.count_words()

    def _is_timestamps_in_time_frame(self, ts, in_time_frame):
        if ts:
            return any([(int(chunk[0]) < ts.timestamp() < int(chunk[1])) for chunk in self._time_frames])
        else:
            return in_time_frame

    def _read_file(self, path):
        """
        :param path: path of a file
        :return: Trie object with all counted word
        """
        print(f'Start examine {path}')
        trie = tri.Trie()
        in_time_frame = False
        with open(path, 'r', buffering=DEFAULT_BUFFER_SIZE) as f:
            for line in f:
                dates_string = utils.find_legal_date(line)
                if dates_string:
                    try:
                        date = list(datefinder.find_dates(dates_string))[0]
                    except (IndexError, OverflowError):
                        date = None
                    if date is not None:
                        in_time_frame = self._is_timestamps_in_time_frame(date, in_time_frame)
                if in_time_frame:
                    for word in line.split():
                        word = self.__char_to_remove.sub('', word.lower())
                        if word in trie:
                            trie[word] += 1
                        else:
                            trie[word] = 1
        print(f'Finish examine {path}')
        return trie

    def _create_summary(self):
        """
        adding all the words appearances into one big Trie
        """
        for file in self.__trie_per_file:
            for word in file:
                if word in self.final_trie:
                    self.final_trie[word] += file[word]
                else:
                    self.final_trie[word] = file[word]

    def _get_all_text_files_paths(self):
        text_files_path = []
        for dirpath, unused_dirnames, filenames in os.walk(LOGS_FOLDER_PATH):
            for filename in filenames:
                if filename.split('.')[-1] in TEXT_FILES_SUFFIXES:
                    text_files_path.append(os.path.join(dirpath, filename))
        print(f'All text files: \n{text_files_path}')
        return text_files_path

    def count_words(self):
        print('Start count words')
        text_files = self._get_all_text_files_paths()
        with Pool(processes=4) as pool:
            self.__trie_per_file = pool.map(self._read_file, text_files)
        self._create_summary()
        top_n = utils.get_top_n_frequent(self.final_trie, self._max_num)
        self.print_summary(top_n)

    def print_summary(self, top_n):
        print(f'Maximum​ {self._max_num}​​ words:')
        for max_value in top_n:
            word = ''.join(max_value[1])
            print(f'Word \'{word}\' occurred {-max_value[0]}')
