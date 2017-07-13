import urllib.request
url = "https://dart.fss.or.kr/dsae001/main.do"
opener = urllib.request.build_opener()
request = urllib.request.Request(url)
response = opener.open(request)
rescode = response.getcode()
