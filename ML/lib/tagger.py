class Tagger(object):

    def featurize(self, words, i, pred_tags):
        raise NotImplementedError

    def predict(self, words):
        raise NotImplementedError