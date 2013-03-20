from gensim.corpora.dictionary import Dictionary
from gensim.models import LsiModel
from gensim.similarities import Similarity

import logging
import sys

from corpus import MsgPackCorpus

def gendict(corpus_path, dict_path,
            words_path="/usr/share/dict/words",
            stopwords_path="data/commonwords.txt",
            no_below=5, no_above=0.5, keep_n=10000):
    dictionary = Dictionary([open(words_path).read().split(), ])
    corpus = MsgPackCorpus(corpus_path, dictionary)

    stopwords = open(stopwords_path).read().split()
    dictionary.filter_tokens([dictionary.token2id[token] for token in stopwords
                                if token in dictionary.token2id])

    dictionary.add_documents([x for x in corpus.get_texts()])

    dictionary.filter_extremes(no_below=no_below, no_above=no_above, keep_n=keep_n)

    dictionary.save(dict_path)


def genmodel(model_path, corpus, dictionary, num_topics):
    model = LsiModel(corpus, id2word=dictionary, num_topics=num_topics)
    model.save(model_path)


def genindex(index_path, model, corpus, num_features):
    index = Similarity(index_path, model[corpus], num_features=num_features)
    index.save()


def usage():
    print 'usage: %s [command] args...' % sys.argv[0]
    print ''
    print 'Commands:'
    print '\tgendict - Generate a dictionary'
    print '\tgenmodel - Generate the LSI model'


def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    corpus_path = "data/corpus.msgpack"
    dict_path = "data/dictionary"
    model_path = "data/model"
    index_path = "data/index"
    
    if len(sys.argv) < 2:
        usage()
        return
    
    if sys.argv[1] == 'gendict':
        print 'Generating Dictionary from corporus %s' % corpus_path
        gendict(corpus_path, dict_path, no_below=2, no_above=0.8, keep_n=30000)
        dictionary = Dictionary.load(dict_path)
    elif sys.argv[1] == 'genmodel':
        print 'Generating LSI model'
        dictionary = Dictionary.load(dict_path)
        corpus = MsgPackCorpus(corpus_path, dictionary)
        genmodel(model_path, corpus, dictionary, num_topics=500)
    elif sys.argv[1] == 'genindex':
        print 'Generating index'
        dictionary = Dictionary.load(dict_path)
        corpus = MsgPackCorpus(corpus_path, dictionary)
        model = LsiModel.load(model_path)
        genindex(index_path, model, corpus, 500)
    else:
        print "Invalid command"
        usage()
        return


if __name__ == "__main__":
    main()
