import http 
from urllib.request import Request, urlopen, HTTPError, URLError
import json
import re

def config_patterns(self, keywords):
        patterns = []

        for keyword in keywords:
            splitted = re.split(r'[- ]', keyword)

            pattern = r'\b(' + r'[ -]?'.join(splitted) + r')\b'

            pattern2 = r'\b('
            for index, word in enumerate(splitted):
                pattern2 += word
                if index != len(splitted) - 1:
                    pattern2 += r'[ -]?'
            pattern2 += r')\b'

            if pattern != pattern2:
                print('wtf??')
                print(pattern)
                print(pattern2)

            patterns.append(pattern)

        return patterns

