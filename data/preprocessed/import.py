from collections import defaultdict
import numpy as np
import re
import pickle

PATH_TO_CRAN_TXT = '../cran/cran.all.1400'
PATH_TO_CRAN_QRY = '../cran/cran.qry'
PATH_TO_CRAN_REL = '../cran/cranqrel'

# Regex to split the text into chuncks at the start of the marker
I_marker = re.compile('\.I.')# for articles and queries
ABTW_marker = re.compile('\.[A,B,T,W]')# for articles
W_marker = re.compile('\.[W]') # for queries

def import_data(PATH_TO_FILE, marker_docId):
  """
  Reads the file and splits the text into entries at the ID marker '.I'.
  The first entry is empty, so it is removed.

  Input:
    PATH_TO_FILE: path to the file to be read
    marker_docId: regex at which we want to split the text
  Output:
    lines: list of strings, each string is an entry of the file

  """
  lines = []
  try:
    with open (PATH_TO_FILE,'r') as f:
      text = f.read().replace('\n'," ")
      lines = re.split(marker_docId,text)
      lines.pop(0) # removes the first empty entry

  except:
      print("File doesn't exist")
      
  return lines
 

def get_text_only(doc, marker_text):
  """
    This function takes as input a list of strings, each string is an entry of the file.
    It splits the text into chunks at the start of each tag, and saves only the entries
    included in the .W tag. Then it removes non-alphabetic characters and non-whitespace
    characters from the text. Finally, it splits the text into words removing the whitespaces.
    It returns a list of lists containing the text in articles.

  """
  doc_tokens = []
  for line in doc:
    #Split the text into chunks at the start of each tag
    entries= re.split(marker_text,line) 
    #Save only entries included in .W tag
    text = entries[4 if len(entries) > 2 else 1]
    #Remove non-alphabetic characters nd non-whitespace characters from text
    text = re.sub(r'[^a-zA-Z\s]+', '', text)
    #text = text.lower() # convert to lowercase
    #For each id, append a list of lists containing the text in articles
    doc_tokens.append(text.split()) # split the text into words removing the whitespaces
  return doc_tokens

txt_list = import_data(PATH_TO_CRAN_TXT, I_marker)
qry_list = import_data(PATH_TO_CRAN_QRY, I_marker)

articles = get_text_only(txt_list, ABTW_marker)
queries = get_text_only(qry_list, W_marker)


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

