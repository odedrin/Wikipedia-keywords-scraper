import re
from timeit import default_timer as timer
import json

class SearchEngine():
    def __init__(self, config):
        self.keywords = self._config_keywords(config['keywords_file'])
        self.patterns = self._config_patterns(self.keywords)

    def search(self, text):
        keyword_set = set()
        for pattern in self.patterns:
            pattern = re.compile(pattern, re.I)
            match = re.search(pattern, text)
            if match:
                keyword_set.add(str.lower(match.group(0)).replace('-', ' '))
        return list(keyword_set)

    def _config_keywords(self, keywords_file):
        try:
            with open(keywords_file, 'r') as f:
                return f.read().replace('(', '\(').replace(')', '\)').split('\n')
        except IOError:
            print('Invalid filename. aborting.')
            exit()

    def _config_patterns(self, keywords):
        patterns = []
        for keyword in keywords:
            splitted_keyword = re.split(r'[- ]', keyword)
            pattern = r'\b(' + r'[ -]?'.join(splitted_keyword) + r')\b'
            patterns.append(pattern)
        return patterns

class Configuration():
    def __init__(self, config_file):
        try:
            with open(config_file) as json_file:
                self.data = json.load(json_file)
        except IOError:
            print('invalid cofiguration file. Aborting')
            exit()

    def __getitem__(self, k):
        return self.data[k]


if __name__ == '__main__':
    config = Configuration('config_file.json')
    engine = SearchEngine(config)
    print(engine.patterns)

    # start = timer()
    # print(engine.search('Welcome to >>GENERAL-motors! We love programming! We are also in the Networks Industrial buisness'))
    # end = timer()
    # print(end - start)
    
    # start = timer()
    # print(engine.search('Welcome to >>GENERAL-motors! We love programming! We are also in the Networks (Industrial) buisness'))
    # end = timer()
    # print(end - start)