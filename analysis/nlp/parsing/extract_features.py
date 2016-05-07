# -*- coding: utf-8 -*-
#
# extract the feature of documents through different methods.
import nltk
import logging
import utilities
from gensim import corpora
from gensim.models import word2vec
from gensim.models.ldamodel import LdaModel
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',)
nltk.data.path.append("/nltk")


def extract_bag_of_words_single(path, stops, toExtract):
    sdata = utilities.read_from_json(path)
    try:
        words = " ".join(sdata[toExtract]).lower().split()
    except:
        words = []
    meaningful_words = [w for w in words if w not in stops]
    return " ".join(meaningful_words)


def extract_bag_of_words_all(paths, maxfeature=5000, toExtract="abstract"):
    # create bag of words features
    stops = set(nltk.corpus.stopwords.words("english"))
    docs = [extract_bag_of_words_single(p, stops, toExtract) for p in paths]
    vectorizer = CountVectorizer(analyzer="word", max_features=maxfeature)
    trained_features = vectorizer.fit_transform(docs)
    trained_features = trained_features.toarray()
    return trained_features


def extract_word_for_word2vec(path, stops, toExtract, cond=False):
    # to train Word2Vec it is better not to remove stop words because the
    # algorithm relies on the broader context of the sentence in order to
    # produce high-quality word vectors.
    sdata = utilities.read_from_json(path)
    try:
        words = " ".join(sdata[toExtract]).lower().split()
    except:
        words = []
    if cond:
        words = [w for w in words if w not in stops]
    return words


def extract_word2vec(paths, toExtract="abstract", num_workers=4,
                        num_features=300, min_word_count=40, context=5,
                        downsampling=1e-3, ifcontinue=False,
                        negative_sampling=0):
    # distributed word vectors
    stops = set(nltk.corpus.stopwords.words("english"))
    sentences = [extract_word_for_word2vec(p, stops, toExtract) for p in paths]
    logging.info("Training model...")
    model = word2vec.Word2Vec(sentences, workers=num_workers, \
                size=num_features, min_count=min_word_count, \
                window=context, sample=downsampling, \
                negative=negative_sampling)
    # If you don't plan to train the model any further, calling
    # init_sims will make the model much more memory-efficient.
    # =no more updates, only querying
    model.init_sims(replace=ifcontinue)
    logging.info("End up training...")
    logging.info("Saving model")

    model_name = ("model/" + "num_workers_" + str(num_workers) + \
                  "_num_of_features_" + str(num_features) + \
                  "_min_count_" + str(min_word_count) + \
                  "_window_size_" + str(context) + \
                  "_downsampling_" + str(downsampling) + \
                  "_negative_sampling_" + str(negative_sampling))
    return model, model_name


def prepare_for_lda(text, stops):
    """Process raw text fot the LDA topic modelling.
    input:
        text: a string
        stops: stops words in english
    """
    tokens = (" ".join(text)).lower().split()
    stopped_tokens = [w for w in tokens if w not in stops]
    p_stemmer = PorterStemmer()
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
    return [stemmed_tokens]


def lda_topic_model(data, is_clean=False, num_of_topics=10, num_of_pass=5):
    """do the topic model for the given dataset
    input:
        data: a documents or a list of words
        is_clean: Use this notation to pre-process the data.
        num_of_topics: An LDA model requires the user to determine how many
                        topics should be generated.
        num_of_pass: The greater the number of passes, the more accurate the
                    model will be.
                    A lot of passes can be slow on a very large corpus.
    """
    if not is_clean:
        stops = set(nltk.corpus.stopwords.words("english"))
        texts = prepare_for_lda(data, stops)
    else:
        texts = data
    dictionary = corpora.Dictionary(texts)
    print dictionary
    corpus = [dictionary.doc2bow(text) for text in texts]
    ldamodel = LdaModel(corpus, id2word=dictionary, num_topics=num_of_topics, \
                        passes=num_of_pass)
    return ldamodel.print_topics(num_topics=num_of_topics, num_words=10)


def test_lda(paths):
    for path in paths:
        sdata = utilities.read_from_json(path)
        lda_topic_model(sdata["body"])
        break


def training_different_word2vec_model(paths, num_thread):
    for num_of_features in [500, 900, 2000, 3000]:
        for negative in [0, 5, 11, 17, 20]:
            for size_content in [4, 6, 8, 10]:
                model, model_name = extract_word2vec(paths, toExtract="abstract",\
                                    num_workers=num_thread, negative_sampling=negative,\
                                    context=size_content)
                model.save(model_name)


def main(in_path):
    paths = utilities.list_files(in_path)
    # logging.info('Test: Extract Bag of words features...')
    # extract_bag_of_words_all(paths)
    logging.info('Extract word2vec features...')
    training_different_word2vec_model(paths, num_thread=4)
    # logging.info('Test: Extract LDA topic model...')
    # test_lda(paths)


if __name__ == '__main__':
    data_in_path = "data/"
    main(data_in_path)
