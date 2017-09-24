# Thematic Index Generater

Introduction:

This is an automatic method for generating thematic index from google trend and google finance data.

 * Step1: Cache Google Trend related topics from a given set of keywords. This is done by recursively querying google trends' "related topics" suggestions for a given search. And then a basic knowledge network of related topics is built with level information from the starting keywords. The query is via the python package pytrends. To do this, simply run *run_cache_google_trend.py*. Google trend data is saved in *cached_google_trend.json* in the *datafile* folder.


 * Step2: Cache Google Finance data. If not done, need to cache all google finance basic information about all public stocks of interest. This is done via query the google finance returned json file. Run *run_cache_google_trend.py* will save basic google finance info into *cached_google_finance.json* in the *datafile* folder. Caching them avoid google server issue that too frequency query might bring.


 * Step3: Generate a score for all stocks cached from Google finance. The score is calculated based on how the google finance description of the company agrees with the google trend knowledge network of related topics built in Step1. General rule: more matching words means higher score; the less the level of the knowledge network from the starting keywords, the higher the score. Run *run_company_score.py* will save the score data into *cached_company_score.json* in the *datafile* folder.


* Step4. Finally, run *build_index_compositions.py* to build the final index with stocks selected and their weights. Final index details saved in *index_compositions.csv* in the *datafile* folder. The google trend relevant score and market cap is combined to genreate a final score. Stocks with both a high score and high market cap are selected. Stocks with high score have high weights.

