from corpus import MsgPackCorpus

from gensim.corpora.dictionary import Dictionary
from gensim.models import LsiModel
from gensim.similarities import MatrixSimilarity

import msgpack

import logging
import sys

def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    dictionary = Dictionary.load("data/nonprofits.dict")
    corpus = MsgPackCorpus("data/nonprofits.msgpack", dictionary)
    lsi = LsiModel.load("data/nonprofits.lsi")

    index = MatrixSimilarity.load("data/nonprofits.index")
    
    doc = "school of public health education"

    lsi_doc = lsi[dictionary.doc2bow(doc.lower().split())]
    sim_ids = index[lsi[dictionary.doc2bow(doc.lower().split())]]
    sim_ids = sorted(enumerate(sim_ids), key=lambda item: -item[1])[:10]
    print sim_ids

    sim_datas = [corpus.get_data(sim_id[0]) for sim_id in sim_ids]
    print sim_datas

if __name__ == '__main__':
    main()
