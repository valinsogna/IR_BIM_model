from collections import defaultdict, OrderedDict
from math import log
import re
# To use nltk, install databases on your machine
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


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
    This function builds an inverted index as an hash table (dictionary)
    where the keys are the terms and the values are ordered lists of
    docIDs containing the term.
    Before inserting the terms in the inverted index, it performs stemming.
    """
    stops=set(stopwords.words('english'))
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
    This function computes the document frequency
    for each term in the inverted index.
    """
    df={}
    for term in index.keys():
        df[term]=len(index[term])
    return df


def inverse_doc_frequency_term(n,doc_frec_term):
    """
    Given the document frequency of a term and the lenght 
    of the collection, this function returns the
    inverse document frequency of that term.
    """
    return log(n/doc_frec_term)


def make_list_query(query):
    """
    Given a free-form text query, this function creates a list 
    containing all the terms present in the query as a string.
    """
    query=re.sub(r'[^a-zA-Z\s]+', '',query)
    list=query.split()
    return list


def print_article(article):
    """
    Given a list of terms (eg. articles, queries) this 
    function prints the document, by joining the 
    terms in the list.
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