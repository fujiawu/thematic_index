"""
This is the module for data library
"""

import csv
import json
import requests
from collections import deque
from pytrends.request import TrendReq
import re


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
    try:
        rsp = requests.get(url)
        raw_data = json.loads(rsp.content[6:-2].decode('unicode_escape'))
        result = dict()
        try:
            result["beta"] = raw_data["beta"]
            result["mktcap"] = raw_data["mc"]
            result["description"] = raw_data['summary'][0]['overview']
        except (RuntimeError, KeyError):
            pass
        return result
    except requests.exceptions.RequestException:
        return None


def google_trend_info(keyword):
    """
    read google trend information on keyword, leverage pytrends package
    :param keyword: any keyword
    :return: result: info return by google trend
    """
    result = dict()
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=[keyword])
    """
    try:
        result["suggestions"] = pytrend.suggestions(keyword=keyword)
    except RuntimeError:
        pass
    try:
        result["related_queries"] = pytrend.related_queries()[keyword]
    except RuntimeError:
        pass
    """
    try:
        result["related_topics"] = pytrend.related_topics()[keyword]
    except (RuntimeError, KeyError):
        pass
    return result


def is_ascii(s):
    """
    check whether a string is ascii string or not
    :param s: input string
    :return: ascii string or not
    """
    return all(ord(c) < 128 for c in s)


def build_google_trend_topic_net(starting_topics, stopping_level, savefilename):
    """
    :param starting_topics: starting topics to search
    :param stopping_level: the level to stop from the starting_topics
    :param savefilename: filename to save query result
    """
    # initialization
    queue = deque()
    searched = dict()
    for key in starting_topics:
        queue.append((key, 0))
        searched[key] = 0

    save_freq = 10

    # run google trend query
    count = 0
    while len(queue):

        keyword, level = queue.popleft()

        if level > stopping_level or not is_ascii(keyword):
            continue

        print 'working on:"' + keyword + '", level:' + str(level)

        gtrend = google_trend_info(keyword)

        if gtrend is None:
            print "Cannot get google trend info for " + keyword
            continue

        try:
            related_topics = gtrend["related_topics"]["title"].tolist()
        except (RuntimeError, KeyError, TypeError):
            continue

        for key in related_topics:
            key = key.lower()
            if key not in searched.keys() and is_ascii(key):
                queue.append((key, level + 1))
                searched[key] = level+1

        count += 1
        if count == save_freq:
            with open("datafile\\" + savefilename, 'w') as fp:
                json.dump(searched, fp)
            count = 0
    with open("datafile\\" + savefilename, 'w') as fp:
        json.dump(searched, fp)


def cache_google_finance_info(savefilename):
    """
    cache google finance info
    :param savefilename: filename for the cache
    :return: none
    """

    try:
        with open("datafile\\" + savefilename, 'r') as fp:
            cached_gfinance_info = json.load(fp)
    except IOError:
        cached_gfinance_info = dict()

    save_freq = 1
    all_stocks = stocks_info_from_exchanges()
    count = 0
    for exchange in all_stocks:
        stocks = all_stocks[exchange]
        for stock in stocks:
            symbol = stock["Symbol"]

            if not is_ascii(symbol):
                continue
            symbol_split = re.split("[\^.*-]+", symbol)
            if len(symbol_split) < 1:
                continue
            symbol = symbol_split[0]
            if exchange+":"+symbol in cached_gfinance_info.keys():
                print "%s exists" % (exchange+":"+symbol)
                continue
            try:
                gfinance_info = google_finance_info(symbol)
            except ValueError:
                try:
                    gfinance_info = google_finance_info(exchange+":"+symbol)
                except ValueError:
                    print "cannot get google finance: ", exchange+":"+symbol
                    continue
            if gfinance_info and "beta" in gfinance_info.keys() \
                and "description" in gfinance_info.keys()\
                    and "mktcap" in gfinance_info.keys():
                item = {"symbol": symbol,
                        "beta": gfinance_info["beta"],
                        "description": gfinance_info["description"],
                        "exchange": exchange,
                        "sector": stock["Sector"],
                        "name": stock["Name"],
                        "industry": stock["industry"],
                        "mktcap": gfinance_info["mktcap"],
                        }
                cached_gfinance_info[exchange+":"+symbol] = item
                print "got %s" % (exchange+":"+symbol)
                count += 1
                if count == save_freq:
                    with open("datafile\\" + savefilename, 'w') as fp:
                        json.dump(cached_gfinance_info, fp)
                    count = 0
                    print "file updated"
    with open("datafile\\" + savefilename, 'w') as fp:
        json.dump(cached_gfinance_info, fp)


def test():
    """Testing Docstring"""
    pass

if __name__ == '__main__':
    test()
