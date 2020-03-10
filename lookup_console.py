#!/usr/bin/python

"""
Console application to quickly lookup words with similar meaning
and add the selected word to the clipboard.
"""

import sys
import argparse
import requests
import configparser
from PyInquirer import prompt
from pyperclip import copy
from itertools import chain


parser = argparse.ArgumentParser()
parser.add_argument("word", help="the word to look up")
parser.add_argument("-d", "--definitions", help="get the definitions", action="store_true", default=False)
arguments = parser.parse_args()

config = configparser.ConfigParser()
config.read('lookup_console.ini')

# Constants
API_KEY = config['API']['api_key']
HEADERS = {
        'x-rapidapi-host': "wordsapiv1.p.rapidapi.com",
        'x-rapidapi-key': API_KEY
    }


def send_request(lookup_word):
    url = f"https://wordsapiv1.p.rapidapi.com/words/{lookup_word}"
    response = requests.get(url, timeout=5, headers=HEADERS)

    if response.status_code != 200:
        print(response)
        sys.exit(1)

    return response.json()['results']


def parse_response(response):
    result = list()
    for res in response:
        definition = res.get('definition', None)
        synonyms = res.get('synonyms', None)
        result.append((definition, synonyms))

    return result


def prompt_result(result):
    if arguments.definitions:
        word_options = [res[0] for res in result]
    else:
        word_options = [synonym for word_data in result for synonym in word_data[1]]

    question = [
        {
            'type': 'list',
            'name': 'selected_word',
            'message': 'Select word to clipboard',
            'choices': word_options
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
