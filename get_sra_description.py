from sys import argv
import requests
from bs4 import BeautifulSoup


def get_name(sra="SRX3345278"):
    resp = requests.get(
        "https://www.ncbi.nlm.nih.gov/sra/?term={0}".format(sra))
    soup = BeautifulSoup(resp.text, 'lxml')
    info = soup.find('p', attrs={'class': 'details expand e-hidden'}).text
    return info


if len(argv) > 1:
    try:
        get_name(sra=argv[1])
    except AttributeError:
        print('Error cannot find sample name {0}'.format(argv[1]))
