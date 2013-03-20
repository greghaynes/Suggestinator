from gensim.corpora.dictionary import Dictionary
from corpus import MsgPackCorpus

import logging
import sys

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


def usage():
    print 'usage: %s [command]' % sys.argv[0]
    print ''
    print 'Commands:'
    print '\tgendict - Generate a dictionary'


def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    corpus_path = "data/corpus.msgpack"
    dict_path = "data/dictionary"
    
    if len(sys.argv) != 2:
        usage()
        return
    
    if sys.argv[1] == 'gendict':
        print 'Generating Dictionary from corporus %s' % corpus_path
        gendict(corpus_path, dict_path, no_below=2, no_above=0.8, keep_n=30000)
        dictionary = Dictionary.load(dict_path)
    else:
        print "Invalid command"
        usage()
        return


if __name__ == "__main__":
    main()
