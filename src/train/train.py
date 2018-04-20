from snownlp import SnowNLP, sentiment

import sys
sys.path.insert(0, "/home/cgz/Projects/taptapcrawl/src")

from models import Review

import codecs
import random

MAX_TRAIN_SIZE = 4000
THRESHOLD = 0.8

def write(reviews, fp):
    with codecs.open(fp, 'w+', encoding="utf8") as f:
        for review in reviews:
            f.write(review.text.replace('\r\n', ' ').replace('\n', ' '))
            f.write('\n')

def filter_length(item):
    return len(item.text) <= 300

def get_pos_reviews():
    pos_reviews = Review.select().where(Review.star > 3)
    print "total %d positive reviews"%len(pos_reviews)
    array = filter(filter_length, pos_reviews)
    result = array[:MAX_TRAIN_SIZE]
    random.shuffle(result)
    return result

def get_neg_reviews():
    neg_reviews = Review.select().where(Review.star < 3)
    print "total %d negitive reviews"%len(neg_reviews)
    array = filter(filter_length, neg_reviews)
    result = array[:MAX_TRAIN_SIZE]
    random.shuffle(result)
    return result

def split(train, ratio=0.8):
    length = len(train)
    train_size = int(length * ratio)
    return train[:train_size], train[train_size:]

def train():
    pos = get_pos_reviews()
    neg = get_neg_reviews()

    pos_train, pos_test = split(pos)
    write(pos_train, "./train/pos_train")
    write(pos_test, "./train/pos_test")

    neg_train, neg_test = split(neg)
    write(neg_train, "./train/neg_train")
    write(neg_test, "./train/neg_test")

    sentiment.train("./train/neg_train", "./train/pos_train")
    sentiment.save('./train/sentiment.marshal')

def test(threshold):
    with codecs.open("./train/neg_test", encoding="utf8") as f:
        content = f.read()
        negs = content.split('\n')

    with codecs.open("./train/pos_test", encoding="utf8") as f:
        content = f.read()
        poss = content.split('\n')

    total = len(negs) + len(poss)
    print "threshold:", threshold
    correct = 0
    for pos in poss:
        if not pos:
            continue
        snow = SnowNLP(pos)
        if snow.sentiments >= threshold:
            correct += 1

    for neg in negs:
        if not neg:
            continue
        snow = SnowNLP(neg)
        if snow.sentiments < threshold:
            correct += 1


    print "total:", total
    print "test result: %2f%%"%(float(correct) / total * 100)

if __name__ == "__main__":
    # train()
    test(THRESHOLD)
