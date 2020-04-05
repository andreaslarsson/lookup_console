import urllib.request
import urllib.error
from http import client
import time
from bs4 import BeautifulSoup
from user_agent import generate_user_agent


class ReferenceBookException(Exception):
    pass


TYPE_TO_SITE = {'syn': 'thesaurus',
                'def': 'dictionary'}


def timeit(method):
    def timed(*args, **kw):
        start_time = time.time()
        result = method(*args, **kw)
        end_time = time.time()

        print(f"{method.__name__} took {end_time - start_time:.3f} seconds")
        return result

    return timed


@timeit
def fetch_html(word, type):
    url = f"https://www.{TYPE_TO_SITE[type]}.com/browse/{word}"
    headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
    request = urllib.request.Request(url, headers=headers)

    try:
        html = urllib.request.urlopen(request, timeout=5).read()
    except urllib.error.HTTPError as e:
        raise ReferenceBookException(f"Exception occurred while fetching data for '{word}': {e.code} - {e.msg}")
    except client.InvalidURL as e:
        raise ReferenceBookException(e)
    
    return html


@timeit
def parse_synonyms_html(html):
    if not html:
        raise ReferenceBookException("Cannot parse empty HTML")

    soup = BeautifulSoup(html, 'html.parser')
    main_content = soup.find('section', attrs={'class': 'MainContentContainer'})
    main_content_section = main_content.find('section')

    description = main_content_section.contents[0].find('strong').text
    result_list = main_content_section.contents[1].find('ul')
    synonyms = [list_item.text for list_item in result_list.findAll('a')]

    return {'description': description, 'synonyms': synonyms}


@timeit
def parse_definitions_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    first_sibling = soup.find('section', attrs={'id': 'top-definitions-section'})

    definitions = list()

    for sibling in first_sibling.next_siblings:
        default_contents = (sibling.find('div', attrs={'class': 'default-content'}))
        definitions.extend([def_div.get_text().strip() for def_div in default_contents if def_div])

    return definitions


def get_synonyms(word):
    synonyms_html = fetch_html(word, 'syn')
    return parse_synonyms_html(synonyms_html)


def get_definitions(word):
    definitions_html = fetch_html(word, 'def')
    return parse_definitions_html(definitions_html)
