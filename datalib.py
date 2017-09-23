"""
This is the module for data library
"""

import csv
import json
import requests


def stocks_info_from_exchanges():
    """
    Read basic stock info from csv file downloaded from exchanges
    """

    exchanges = ["NYSE", "NASDAQ", "AMEX"]
    stockinfo = dict()

    for exchange in exchanges:
        filename = "datafile\\" + exchange + ".csv"
        symbols = []
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                symbols.append(row.copy())
                stockinfo[exchange] = symbols
    return stockinfo


def google_finance_info(symbol):
    """
    Read text info from google finance
    :param symbol:
    :return: dict
    """
    url = "https://finance.google.com/finance?q=" + symbol + "&output=json"
    rsp = requests.get(url)
    raw_data = json.loads(rsp.content[6:-2].decode('unicode_escape'))
    result = dict()
    result["beta"] = raw_data["beta"]
    result["description"] = raw_data['summary'][0]['overview']
    return result


def test():
    """Testing Docstring"""
    pass

if __name__=='__main__':
    test()
