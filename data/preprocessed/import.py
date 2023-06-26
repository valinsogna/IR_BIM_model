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
    Splits the text into chunks at the start of each tag, and saves only the entries included in the '.W' tag. 
    Then it removes non-alphabetic characters and non-whitespace.

    Input:
      doc: list of strings, each string is an entry of the file
      marker_text: regex at which we want to split the text
    Output:
      doc_tokens: list of lists, each list contains the text of an entry of the file
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


def import_relevance(PATH_TO_FILE):
  """
  Imports all the relevant articles for each query, returning a dictionary.
  The keys are the IDs (numbers) of the queries and the values are tuples containing docIDs of the relevant documents to that query along with the degrees of relevance.
  It is used to give user feedback in the relevance feedback.

  Input:
    PATH_TO_FILE: path to the file to be read
  Output:
    relevance: dictionary

  The degrees are defined by Cleverdon as follows:
    1.  References which are a complete answer to the question.
    2.  References of a high degree of relevance, the lack of which
        either would have made the research impracticable or would
        have resulted in a considerable amount of extra work.
    3.  References which were useful, either as general background
        to the work or as suggesting methods of tackling certain aspects
        of the work.
    4.  References of minimum interest, for example, those that have been
        included from an historical viewpoint.
    5.  References of no interest.
    P.S. Obviously no 5's are included in the qrels.
  """
  cran_rel_data = None

  try:
    cran_rel_data = open(PATH_TO_FILE, 'r')
  except:
    print("File doesn't exist")

  cran_np = np.loadtxt(cran_rel_data, dtype=int)

  relevance = defaultdict(set)
  for row in cran_np:
    relevance[row[0]].add(tuple(row[1:]))
    
  return relevance


txt_list = import_data(PATH_TO_CRAN_TXT, I_marker)
qry_list = import_data(PATH_TO_CRAN_QRY, I_marker)

articles = get_text_only(txt_list, ABTW_marker)
queries = get_text_only(qry_list, W_marker)
relevance = import_relevance(PATH_TO_CRAN_REL)

with open("articles.pkl",'wb') as f:
    pickle.dump(articles,f)

with open("queries.pkl",'wb') as f:
    pickle.dump(queries,f)

with open("relevance.pkl",'wb') as f:
    pickle.dump(relevance,f)