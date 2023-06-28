from collections import defaultdict, OrderedDict
from math import log
import re
# To use nltk, install databases on your machine
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
#nltk.download('punkt')
from nltk.tokenize import word_tokenize
import string

punctuation = set(string.punctuation)

def stemming(list):
    """
    Given a list of terms, this function performs 
    the stemming of each term present in the list.
    """
    stemmer=PorterStemmer()
    list=[stemmer.stem(term) for term in list]
    return list


def make_inverted_index(articles):
    """
    Creates and returns the inverted index from the articles as an hash table
    where the keys are the terms and the values are ordered lists of
    docIDs containing the term.
    It performs stemming, and stopword removal.
    """
    stops=set(stopwords.words('english'))
    # Add some words to the stopwords set
    stops.update(['isn', 'won', 're', 'll' ]) # s, t already in stopwords
    index = defaultdict(set) 
    for docid, article in enumerate(articles): 
        article=stemming(article)
        for term in article:
            if term not in stops:

                index[term].add(docid)

    index=OrderedDict(sorted(index.items()))
    return index


def doc_frequency(index):
    """
    Calculates and returns the document frequency for each term in the inverted index.
    """
    doc_frequency={}
    for term in index.keys():
        doc_frequency[term]=len(index[term])
    return doc_frequency


def inverse_doc_frequency_term(n,doc_frec_term):
    """
    Given the document frequency of a term and the lenght 
    of the collection, this function returns the
    inverse document frequency of that term.
    """
    return log(n/doc_frec_term)


def make_tokens(query):
    """
    Given a free-form text query, this function creates a list 
    containing all the terms present in the query as a string.
    """

    # Set to lowercase the terms in text and remove '-' from text to avoid words like 'non-linear' to be considered as a single word.
    query = query.replace('-', ' ').casefold() # casefold is more aggressive that lower() (e.g. ß -> ss)

    # Tokenize the text and remove non-alphabetical characters and empty strings and punctuation from tokens
    tokens = [re.sub(r'[^a-z]', '', word) for word in word_tokenize(query) if word not in punctuation]
    # Remove empty strings and 1 and 2 characters strings from tokens usigna regex:
    #tokens = [re.sub(r'^.{1,2}$', '', word) for word in tokens]
    #tokens = [re.sub(r'^.{1}$', '', word) for word in tokens]
    tokens = list(filter(None, tokens))
    return tokens

def print_txt(article):
    """
    Given a list of terms (eg. articles, queries) this 
    function prints the document, by joining the 
    terms in the list separating them by whitespaces.
    """
    article=" ".join(article)
    print(article)


def get_list(elem_list, query):
    """
    This function is used to create a sublist made of choosen 
    elements from a list. It is used to choose the queries and
    the relative relevant documents in the mean average precision function.
    """
    return [query[i] for i in elem_list]