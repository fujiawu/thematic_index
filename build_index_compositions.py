
import json
import csv

jsonsavefilename = "cached_company_score.json"
with open("datafile\\" + jsonsavefilename, 'r') as fp:
    stock_scores = json.load(fp)

stock_list = []
for symbol in stock_scores:
    item = stock_scores[symbol]
    item["symbol"] = symbol
    stock_list.append(item)
stock_list = sorted(stock_list, key=lambda k: k['score'], reverse=True)

keys = stock_list[0].keys()
csvfilename = "index_compositions.csv"
with open("datafile\\" + csvfilename, 'wb') as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(stock_list)


