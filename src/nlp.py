from snownlp import SnowNLP

THRESHOLD = 0.8

def is_possitive(doc):
    snow = SnowNLP(doc)
    return snow.sentiments > THRESHOLD
