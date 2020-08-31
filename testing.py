import http 
from urllib.request import Request, urlopen, HTTPError, URLError
import json

data = {
    "num_of_workers": 3,
 'rps': 5,
  'url_gen': 'https://en.wikipedia.org/wiki/Special:Random',
   'keyword_file': 'keywords.txt'}
with open('config_file.json', 'w') as outfile:
    json.dump(data, outfile)

