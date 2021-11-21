import requests


def get_word(address):
    URL = "https://kpolyakov.spb.ru/cms/files/{}".format(address)
    response = requests.get(URL)
    return response.content
