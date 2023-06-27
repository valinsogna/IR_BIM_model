from collections import defaultdict
import numpy as np
import re
import pickle
import string
# To use nltk, install databases on your machine
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

PATH_TO_CRAN_TXT = '../cran/cran.all.1400'
PATH_TO_CRAN_QRY = '../cran/cran.qry'
PATH_TO_CRAN_REL = '../cran/cranqrel_bin.txt'

# Regex to split the text into chuncks at the start of the marker
I_marker = re.compile('\.I.')# for articles and queries
ABTW_marker = re.compile('\.[ABTW]')# for articles
W_marker = re.compile('\.[W]') # for queries

punctuation = set(string.punctuation)

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
 

def get_text_only(txt_list, marker_text):
  """
    It removes punctuation, divide strings by char '-', converts the text to lowercase and removes non alphabetical characters.
    It returns a list of lists, each list contains the text content (the one inside .W tag) of an entry of the file txt_list.

    Input:
      txt_list: list of strings, each string is an entry of the file.
      marker_text: regex at which we want to split the text
    Output:
      doc_tokens: list of list of tokens for each article. Each token is a lowercase string and punctuation is removed.
  """

  docs_tokens = []

  for line in txt_list:
      # Split the text into chunks at the start of each tag
      entries = re.split(marker_text, line)

      # Save only entries included in .W tag
      text_content = entries[4] if len(entries) > 2 else entries[1]

      # Set to lowercase the terms in text and remove '-' from text to avoid words like 'non-linear' to be considered as a single word.
      text_content = text_content.replace('-', ' ').casefold() # casefold is more aggressive that lower() (e.g. ß -> ss)

      # Tokenize the text and remove non-alphabetical characters and empty strings and punctuation from tokens
      tokens = [re.sub(r'[^a-z]', '', word) for word in word_tokenize(text_content) if word not in punctuation]
      # Remove empty strings and 1 and 2 characters strings from tokens usigna regex:
      #tokens = [re.sub(r'^.{1,2}$', '', word) for word in tokens]
      tokens = [re.sub(r'^.{1}$', '', word) for word in tokens]
      #tokens = list(filter(None, tokens))
      docs_tokens.append(tokens)

  return docs_tokens


def import_relevance(PATH_TO_FILE):
  """
  Imports all the relevant articles for each query, returning a dictionary.
  The keys are the IDs (numbers) of the queries and the values are the docIDs only 
  of the relevant documents to that query (aka the one with forth column value 1).
  It is used to give user feedback in the relevance feedback.

  Input:
    PATH_TO_FILE: path to the file to be read
  Output:
    relevance: dictionary
  """
  cran_rel_data = None

  try:
    cran_rel_data = open(PATH_TO_FILE, 'r')
  except:
    print("File doesn't exist")

  cran_np = np.loadtxt(cran_rel_data, dtype=int)

  relevance = defaultdict(set)
  for row in cran_np:
    if row[3] == 1:
      relevance[row[0]-1].add(row[2]-1) # -1 because the IDs for queries and docs start from 1
  
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