#!/usr/bin/python
from word_counter_part2.models import WordCounter, Parser


def main():
    WordCounter(Parser().args)


if __name__ == '__main__':
    main()
