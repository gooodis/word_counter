#!/usr/bin/python
from models import WordCounter, Parser


def main():
    WordCounter(Parser().args)


if __name__ == '__main__':
    main()
