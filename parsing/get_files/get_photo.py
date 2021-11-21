import requests


def get_photo(address):
    URL = "https://kpolyakov.spb.ru/cms/images/{}".format(address)
    response = requests.get(URL)
    return response.content
