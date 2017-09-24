
from algolib import *
import json


def mktcap_parser(s):
    """
    :param s: input string
    :return: numeric value, unit $
    a helper function to parse mkt cap to float, with unit $
    """
    s = s.replace("*", "")
    lookup = {'k': 1000, 'm': 1000000, 'b': 1000000000, 't': 1000000000000}
    unit = s[-1].lower()
    number = float(s[:-1])
    if unit in lookup:
        return lookup[unit] * number
    return number

# read cached google trend
gtrend_filename = "cached_google_trend.json"
with open("datafile\\" + gtrend_filename, 'r') as fp:
    gtrend_topics = json.load(fp)

# read cached google finance
gfinance_filename = "cached_google_finance.json"
with open("datafile\\" + gfinance_filename, 'r') as fp:
    gfinance_stocks = json.load(fp)

# read previously computed company score
jsonsavefilename = "cached_company_score.json"
try:
    with open("datafile\\" + jsonsavefilename, 'r') as fp:
        stock_scores = json.load(fp)
except IOError:
    stock_scores = dict()

# start computing
count = 0
limit = 1000000
for fullsymbol in gfinance_stocks:

    if fullsymbol in stock_scores.keys():
        print fullsymbol + " exists"
        continue

    stock = gfinance_stocks[fullsymbol]
    description = stock["description"]
    matched = find_word_match(description, gtrend_topics)
    score = compute_score(matched)
    try:
        stock_scores[fullsymbol] = {"score": score, "name": stock["name"], "beta": stock["beta"],
                                    "mktcap": mktcap_parser(stock["mktcap"])}
    except (ValueError, IndexError):
        continue
    print "%s,%s,%2.2f,%s(%f)" % (fullsymbol, stock["name"], score, stock["mktcap"],
                                  stock_scores[fullsymbol]["mktcap"])
    with open("datafile\\" + jsonsavefilename, 'w') as fp:
        json.dump(stock_scores, fp)
    count += 1
    if count > limit:
        break
