def photo(adress):
    import requests
    HEADERS = {'user-agent': 'ozilla/5.0 (Windows NT 10.0; Win64; x64)\
     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
               'accept': '*/*'}
    URL = "https://kpolyakov.spb.ru/cms/images/{}".format(adress)
    p = requests.get(URL)
    return p.content


def excel(adress):
    import requests
    URL = "https://kpolyakov.spb.ru/cms/files/{}".format(adress)
    p = requests.get(URL)
    return p.content


def word(adress):
    import requests
    URL = "https://kpolyakov.spb.ru/cms/files/{}".format(adress)
    p = requests.get(URL)
    return p.content
