import re
from timeit import default_timer as timer
import json

class SearchEngine():
    def __init__(self, config):
        self.keywords = self.config_keywords(config.data['keywords_file'])
        self.patterns = self.config_patterns(self.keywords)

    def search(self, text):
        keyword_set = set()
        for pattern in self.patterns:
            pattern = re.compile(pattern, re.I)
            match = re.search(pattern, text)
            if match:
                keyword_set.add(str.lower(match.group(0)).replace('-', ' '))
        return list(keyword_set)

    def config_keywords(self, keywords_file):
        try:
            with open(keywords_file, 'r') as f:
                return f.read().split('\n')
        except IOError:
            print("Invalid filename. aborting.")
            exit()

    def config_patterns(self, keywords):
        patterns = []
        for keyword in keywords:
            splitted = re.split(r'[- ]', keyword)
            pattern = r'\b('
            for index, word in enumerate(splitted):
                pattern += word
                if index != len(splitted) - 1:
                    pattern += r'[ -]?'
            pattern += r')\b'
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


if __name__ == "__main__":
    config = Configuration('config_file.json')
    engine = SearchEngine(config)
    start = timer()
    print(engine.search('Welcome to >>GENERAL-motors! We love programming!'))
    end = timer()
    print(end - start)
    
    start = timer()
    print(engine.search('Beside being a team focused on cyber-security, cybersecurity and cyber security we also do software engineering. With good communication we might figure out some unsolved problems in computer-science!'))
    end = timer()
    print(end - start)