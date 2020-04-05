"""
Console application to quickly lookup words with similar meaning
and add the selected word to the clipboard.
"""

import sys
import argparse
from PyInquirer import prompt
from pyperclip import copy
import reference_book


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


def get_synonyms(word):
    try:
        result = reference_book.get_synonyms(word)
    except reference_book.ReferenceBookException as e:
        print(e)
        sys.exit(1)

    selected_word = prompt_result(result.get('synonyms', None))
    copy(selected_word)


def get_definitions(word):
    try:
        result = reference_book.get_definitions(word)
    except reference_book.ReferenceBookException as e:
        print(e)
        sys.exit(1)

    print(f"\nDefinitions for {word}:")
    print(*result, sep="\n")


parser = argparse.ArgumentParser()
parser.add_argument("word", help="the word to look up")
parser.add_argument('-d', dest='action',
                    action='store_const',
                    const=get_definitions,
                    default=get_synonyms,
                    help='get definitions (default: get synonyms)')

arguments = parser.parse_args()


if __name__ == '__main__':
    arguments.action(arguments.word)
