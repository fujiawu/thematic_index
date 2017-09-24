from datalib import *

starting_topics = ["3d print", "3d printing", "3d printer"]
stopping_level = 10
savefilename = "3d_printer.json"
build_google_trend_topic_net(starting_topics, stopping_level, savefilename)

