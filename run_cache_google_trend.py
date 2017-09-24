from datalib import *

starting_topics = ["additive manufacturing", "rapid manufacturing", "rapid prototyping",
                   "on-demand manufacturing", "3d printing", "3d scanner","AMF", "CAD",
                   "metal wire", "3d model", "3d modeling", "computer-aided design",
                   "computer aided design", "filament", "agile tooling"]
stopping_level = 10
savefilename = "cached_google_trend.json"
build_google_trend_topic_net(starting_topics, stopping_level, savefilename)

