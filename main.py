from corpus import MsgPackCorpus

from gensim.corpora.dictionary import Dictionary
from gensim.models import LsiModel

import msgpack

def main():
    dictionary = Dictionary.load("data/nonprofits.dict")
    corpus = MsgPackCorpus("data/nonprofits.msgpack", dictionary)
    lsi = LsiModel.load("data/nonprofits.lsi")
    

if __name__ == '__main__':
    main()
