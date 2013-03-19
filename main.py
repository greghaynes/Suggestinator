from corpus import MsgPackCorpus

from gensim.corpora.dictionary import Dictionary
from gensim.models import LsiModel
from gensim.similarities import Similarity

import msgpack

from flask import Flask, request

import logging
import sys
import json

app = Flask(__name__)

dictionary = Dictionary.load("data/nonprofits.dict")
corpus = MsgPackCorpus("data/nonprofits.msgpack", dictionary)
lsi = LsiModel.load("data/nonprofits.lsi")

index = Similarity.load("data/index")

def get_suggested_orgs(doc):
    lsi_doc = lsi[dictionary.doc2bow(doc.lower().split())]
    sim_ids = index[lsi[dictionary.doc2bow(doc.lower().split())]]
    sim_ids = sorted(enumerate(sim_ids), key=lambda item: -item[1])[:10]
    sim_datas = [corpus.get_data(sim_id[0]) for sim_id in sim_ids]
    return sim_datas
    

@app.route("/suggestions/orgs", methods=['POST'])
def org_suggestions():
    doc = request.json['doc']
    return json.dumps({'org_ids': get_suggested_orgs(doc)})


@app.route("/index/add_org", methods=['POST'])
def add_org():
    org_id = request.json['id']
    org_doc = request.json['doc']

    corpus.add_text(org_doc, org_id)
    lsi_doc = lsi[(dictionary.doc2bow(org_doc.lower().split()),)]
    index.add_documents(lsi_doc)
    return json.dumps({'status': 'success'})


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    app.run()
