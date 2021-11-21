import requests


def get_excel(address):
    URL = "https://kpolyakov.spb.ru/cms/files/{}".format(address)
    response = requests.get(URL)
    return response.content
