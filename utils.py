from gensim.corpora.dictionary import Dictionary
from corpus import MsgPackCorpus

import logging

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


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    corpus_path = "data/corpus.msgpack"
    dict_path = "data/dictionary"
    gendict(corpus_path, dict_path, no_below=2, no_above=0.8, keep_n=30000)
    dictionary = Dictionary.load(dict_path)
    print dictionary
