#!/usr/bin/python

"""
Console application to quickly lookup words with similar meaning
and add the selected word to the clipboard.
"""

import sys
import argparse
import requests
from PyInquirer import prompt
from pyperclip import copy

parser = argparse.ArgumentParser()
parser.add_argument("word", help="the word to look up")
arguments = parser.parse_args()


def send_request(lookup_word):
    url = f"https://api.datamuse.com/words?ml={lookup_word}"
    response = requests.get(url, timeout=5)

    if response.status_code != 200:
        print(response)
        sys.exit(1)

    return response.json()


def parse_response(response):
    words = list()
    for word in response:
        words.append(word['word'])

    return words


def prompt_result(result):
    question = [
        {
            'type': 'list',
            'name': 'selected_word',
            'message': 'Select word to clipboard',
            'choices': result,
            'filter': lambda val: val.lower()
        }
    ]

    return prompt(question)['selected_word']


def lookup(word):
    response = send_request(word)
    result = parse_response(response)
    selected_word = prompt_result(result)
    copy(selected_word)


if __name__ == '__main__':
    lookup(arguments.word)
