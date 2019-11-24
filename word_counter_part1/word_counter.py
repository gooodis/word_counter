#!/usr/bin/python
from word_counter_part1.models import Parser, WordCounter


def main():
    WordCounter(Parser().args)


if __name__ == '__main__':
    main()

