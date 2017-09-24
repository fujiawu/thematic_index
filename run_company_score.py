
from algolib import *
import json

gtrend_filename = "cached_google_trend.json"
with open("datafile\\" + gtrend_filename, 'r') as fp:
    gtrend_topics = json.load(fp)

gfinance_filename = "cached_gfinance_info.json"
with open("datafile\\" + gfinance_filename, 'r') as fp:
    gfinance_stocks = json.load(fp)

jsonsavefilename = "cached_company_score.json"
try:
    with open("datafile\\" + jsonsavefilename, 'r') as fp:
        stock_scores = json.load(fp)
except IOError:
    stock_scores = dict()

count = 0
limit = 1000000
for stock in gfinance_stocks:
    if stock["symbol"] in stock_scores.keys():
        continue
    description = stock["description"]
    matched = find_word_match(description, gtrend_topics)
    score = compute_score(matched)
    stock_scores[stock["symbol"]] = {"exchange": stock["exchange"], "score": score, "name": stock["name"], "beta": stock["beta"]}
    print "%s-%s,%s,%2.2f" % (stock["exchange"], stock["symbol"].replace(" ", ""), stock["name"], score)
    with open("datafile\\" + jsonsavefilename, 'w') as fp:
        json.dump(stock_scores, fp)
    count += 1
    if count > limit:
        break

