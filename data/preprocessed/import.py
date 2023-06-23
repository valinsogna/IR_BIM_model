import re
from collections import defaultdict, OrderedDict
import pickle

PATH_TO_CRAN_TXT = '../cran/cran.all.1400'
PATH_TO_CRAN_QRY = '../cran/cran.qry'
PATH_TO_CRAN_REL = '../cran/cranqrel'


def import_dataset():
    """
    This function imports all the articles in the Cranfield collection,
    returning list of lists where each sub-list contains all the
    terms (from .T and .W tags) present in each article as a string.
    """

    # Saves the articles in a list of lists, where each sub-list is created after a .I row and it contains all the terms inside .T and .W tags.
    articles = []
    with open('../cran/cran.all.1400', 'r') as f:
        tmp = []
        for row in f:
            if row.startswith(".I"):
                if tmp != []:
                    articles.append(tmp)
                tmp = []
            elif row.startswith(".W"):
                continue
            elif row.startswith(".T"):
                continue
            else:
                #If row starts with .A or .B don't add the folowing lines to the tmp list
                if row.startswith(".A") or row.startswith(".B"):
                    continue
                row = re.sub(r'[^a-zA-Z\s]+', '', row) # removes all the non-alphabetic characters
                tmp += row.split()
        articles.append(tmp)   
    return articles


def import_queries():
    """
    This function imports all the queries in the Cranfield test collection,
    returning list of lists where each sub-list contains all the
    terms present in each query as a string.
    """
    queries = []
    with open('../cran/cran.qry', 'r') as f:
        tmp = []
        for row in f:
            if row.startswith(".I"):
                if tmp != []:
                    queries.append(tmp)
                tmp = []
            elif row.startswith(".W"):
                continue
            else:
                row = re.sub(r'[^a-zA-Z\s]+', '', row) 
                tmp += row.split()
        queries.append(tmp)
    return queries


def import_relevance():
    """
    This function imports all the relevant articles for each query 
    of the Cranfiled test collection, returning a dictionary in 
    which the keys are the IDs (numbers) of the queries and 
    the values are the docIDs of the relevant documents to that query.
    It is used to give user feedback in the relevance feedback.
    """
    relevance=defaultdict(set)
    with open('../cran/cranqrel', 'r') as f:
        for row in f:
            tmp=re.split(r"\s+", row)
            relevance[int(tmp[0])-1].add(int(tmp[2])-1)
    return relevance


# articles=import_dataset()
# queries=import_queries()
# relevance=import_relevance()

# with open("Data/articles.pkl",'wb') as f:
#     pickle.dump(articles,f)

# with open("Data/queries.pkl",'wb') as f:
#     pickle.dump(queries,f)

# with open("Data/relevance.pkl",'wb') as f:
#     pickle.dump(relevance,f)

