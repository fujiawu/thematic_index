"""
This is the module for data library
"""

import csv
import json
import requests
from pytrends.request import TrendReq


def stocks_info_from_exchanges():
    """
    read basic stock info from csv file downloaded from exchanges
    :return: all stock info from csv
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
    read text info from google finance
    :param symbol: stock symbol
    :return: result: info read from google finance
    """
    url = "https://finance.google.com/finance?q=" + symbol + "&output=json"
    rsp = requests.get(url)
    raw_data = json.loads(rsp.content[6:-2].decode('unicode_escape'))
    result = dict()
    result["beta"] = raw_data["beta"]
    result["description"] = raw_data['summary'][0]['overview']
    return result


def google_trend_info(keyword):
    """
    read google trend information on keyword, leverage pytrends package
    :param keyword: any keyword
    :return: result: info return by google trend
    """
    result = dict()
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=[keyword])
    result["suggestions"] = pytrend.suggestions(keyword=keyword)
    result["related_quries"] = pytrend.related_queries()
    result["related_topics"] = pytrend.related_topics()
    return result


def test():
    """Testing Docstring"""
    pass

if __name__=='__main__':
    test()
