import re
from part2 import get_data

def main(keywordsfile, text):
    keywords = configurate(keywordsfile)
    pattern = create_pattern(keywords)
    keywords_set = find_keywords(text, pattern)
    return list(keywords_set)

def configurate(keywordsfile):
    try:
        with open('keywords.txt', 'r') as f:
            return f.read().split('\n')
    except IOError:
        print("Invalid keywords file. aborting.")
        exit()


def create_pattern(keywords):
    pattern = r'\b('
    for index, word in enumerate(keywords):
        for char in word:
            if char == '-' or char == ' ':
                pattern += r'[ -]?'
            elif char.isalpha():
                pattern += char
        if index != len(keywords) - 1:
            pattern += '|'
    pattern += r')\b'
    return pattern

def find_keywords(text, pattern):
    keyword_set = set()
    pattern = re.compile(pattern, re.I)
    matches = re.finditer(pattern, text)
    for match in matches:
        word = str.lower(match.group(0)).replace('-', ' ')
        keyword_set.add(word)

    return keyword_set



if __name__ == "__main__":
    text = get_data('https://en.wikipedia.org/wiki/General_Motors')
    found = main('keywords.txt', text)
    print(found)
