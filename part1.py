import re
import json

class Configuration():
    ''' A class used for the configuration of SearchEngine or ScraperManager. ''' 
    def __init__(self, config_file):
        ''' Requires valid json configuration file. '''
        try:
            with open(config_file) as json_file:
                self.data = json.load(json_file)
        except IOError:
            print('invalid configuration file. Aborting')
            exit()

    def __getitem__(self, k):
        return self.data[k]

class SearchEngine():
    ''' 
    A class used to search text for a list of keywords.
    
    After initializing a SearchEngine, Use the search method.
    '''
    def __init__(self, config: Configuration):
        ''' Requires Configuration instance with a valid 'keywords file' item. '''
        keywords = self._config_keywords(config['keywords file'])
        self._patterns = self._config_patterns(keywords)

    def search(self, text: str):
        ''' Search text for keywords from keywords file, return a list of matches '''
        matches_set = set()
        for pattern in self._patterns:
            match = re.search(pattern, text)
            if match:
                matches_set.add(str.lower(match.group(0)).replace('-', ' '))
        return list(matches_set)

    def _config_keywords(self, keywords_file):
        try:
            with open(keywords_file) as f:
                return f.read().split('\n')
        except IOError:
            print('Invalid filename. Aborting.')
            exit()

    def _config_patterns(self, keywords):
        patterns = []
        translate_table = { ord('('): '\\(', ord(')'): '\\)' }
        for keyword in keywords:
            splitted_keyword = re.split(r'[- ]', keyword)
            pattern = r'\b(' + r'[ -]?'.join(splitted_keyword).translate(translate_table) + r')(?!\w)'
            pattern = re.compile(pattern, re.I)
            patterns.append(pattern)
        return patterns

if __name__ == '__main__':
    config = Configuration('config_file.json')
    searchengine = SearchEngine(config)
    text = 'Beside being a team focused on cyber-security. we also do software engineering. With good communication we might figure out some unsolved problems in computer-science!'
    keywords_found_in_text = searchengine.search(text)
    print(keywords_found_in_text)
    