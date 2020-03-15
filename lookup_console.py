#!/usr/bin/python

"""
Console application to quickly lookup words with similar meaning
and add the selected word to the clipboard.
"""

import sys
import argparse
from PyInquirer import prompt
from pyperclip import copy
import reference_book


parser = argparse.ArgumentParser()
parser.add_argument("word", help="the word to look up")
# parser.add_argument("-d", "--definitions", help="get the definitions", action="store_true", default=False)
arguments = parser.parse_args()


def prompt_result(result):
    question = [
        {
            'type': 'list',
            'name': 'selected_word',
            'message': 'Select word to clipboard',
            'choices': result
        }
    ]

    return prompt(question)['selected_word']


def lookup(word):
    try:
        result = reference_book.get_synonyms(word)
    except reference_book.ReferenceBookException as e:
        print(e)
        sys.exit(1)

    selected_word = prompt_result(result.get('synonyms', None))
    copy(selected_word)


if __name__ == '__main__':
    lookup(arguments.word)
