def get_photo(address):
    import requests
    URL = "https://kpolyakov.spb.ru/cms/images/{}".format(address)
    print(address)
    response = requests.get(URL)
    return response.content


def get_excel(address):
    import requests
    URL = "https://kpolyakov.spb.ru/cms/files/{}".format(address)
    response = requests.get(URL)
    return response.content


def get_word(address):
    import requests
    URL = "https://kpolyakov.spb.ru/cms/files/{}".format(address)
    response = requests.get(URL)
    return response.content
