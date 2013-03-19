from gensim.corpora.textcorpus import TextCorpus

import msgpack

class MsgPackCorpus(TextCorpus):

    def __init__(self, path, dictionary):
        """
        Create a corpus backed by a msgpack file

        The format of the msgpack file should be a sequence of packed objects
        where each object is a tuple of ('text', DATA).
        """
        # Dont call __init__ so we can setup our own dict
        self.path = path
        self.dictionary = dictionary
        self.length = None
        self.data_map = {}

    def scan_src(self):
        unpacker = msgpack.Unpacker(open(self.path))
        self.length = 0
        for u in unpacker:
            self.data_map[self.length] = u[1]
            self.length = self.length + 1

    def __len__(self):
        if self.length == None:
            self.scan_src()
        return self.length

    def get_texts(self):
        self.length = 0
        unpacker = msgpack.Unpacker(open(self.path))
        for u in unpacker:
            self.data_map[self.length] = u[1]
            self.length += 1
            yield [x for x in u[0].lower().split() if x in self.dictionary.token2id]

    def __getitem__(self, index):
        unpacker = msgpack.Unpacker(self.path)
        for i, u in enumerate(unpacker):
            if i == index:
                return u[0]
                break
        raise IndexError("index %d larger than number of documents" % index)
    
    def get_data(self, index):
        if self.length == None:
            self.scan_src()
        return self.data_map[index]
