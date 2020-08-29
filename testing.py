import http 
from urllib.request import Request, urlopen, HTTPError, URLError

url = 'https://en.wikipedia.org/wiki/Special:Random'
request = Request(url)
response = urlopen(request)
print(request.full_url)
for _ in range(15):
    html = str(response.readline())
    print(html)
response.close()

