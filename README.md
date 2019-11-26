# Word Counter Assignment

## Installation & Editing
1. Open Terminal
1. Fork this repo 
1. Install homebrew with the command:
   `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
1. Install Python with Brew
   `brew install python`
1. run `python3 -m venv /path/to/new/virtual/environment`
1. enable venv `source /path/to/new/virtual/environment/bin/activate`
1. change dir to word_counter `cd word_counter`
1. run `pip3 install -r requierments.txt`

## Running Max word
In order to run word count app you should download the executable file located in each one of the folders and follow the instruction below.

In part 1:
  run - `./max_word <number_of_the_maximum_appearnces_word> <path> <path> etc...`
  Example: `$ max-words 5 /tmp /home/user/file.txt`

In part 2:
  run - `./max_word <number_of_the_maximum_appearnces_word> <time stamp> - <time stamp>, ....`
  Example: Human readable: Sat Sep 23 00:34:37 - Sun Sep 24 00:34:37
           Timestamp: 1506200432 - 1506286832
