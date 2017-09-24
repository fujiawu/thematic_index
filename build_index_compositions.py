
import json
import csv
import pprint

# read cached company score
jsonsavefilename = "cached_company_score.json"
with open("datafile\\" + jsonsavefilename, 'r') as fp:
    stock_scores = json.load(fp)

# number of stocks to be selected
num_of_stocks = 100
score_threshold = 2

# get a list of all stocks with scores
stock_list = []
for symbol in stock_scores:
    item = stock_scores[symbol]
    item["symbol"] = symbol
    if item["score"] >= score_threshold:
        stock_list.append(item)

# normalize score and mktcap
count = 0
total_weight = 0
total_mktcap = 0
for stock in stock_list:
    total_weight += stock["score"]
    total_mktcap += stock["mktcap"]
for stock in stock_list:
    stock["normalized_score"] = stock["score"] / total_weight
    stock["normalized_mktcap"] = stock["mktcap"] / total_mktcap
    stock["final_score"] = stock["normalized_score"] + stock["normalized_mktcap"] ** 0.0001

# score company by list
stock_list = sorted(stock_list, key=lambda k: k['final_score'], reverse=True)

# select final stocks
selected_stock_list = []
count = 0
total_final_score = 0
pp = pprint.PrettyPrinter(indent=4)
for stock in stock_list:
    selected_stock_list.append(stock)
    total_final_score += stock["final_score"]
    count += 1
    if count > num_of_stocks:
        break

# compute final weight
final_list = []
for stock in selected_stock_list:
    weight = stock["final_score"] / total_final_score
    item = {"symbol": stock["symbol"], "exchange": stock["exchange"],
            "name": stock["name"], "weight": weight,
            "score": stock["score"],
            "mktcap": stock["mktcap"]}
    final_list.append(item)
    pp.pprint(item)

# dump to csv
keys = final_list[0].keys()
csvfilename = "index_compositions.csv"
with open("datafile\\" + csvfilename, 'wb') as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(final_list)

