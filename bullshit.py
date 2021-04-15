def photo(adress):
    import requests
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
