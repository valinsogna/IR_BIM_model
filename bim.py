from math import log 
import pickle
from utils.functions import *

class BIM_IRModel():
    """
    This class represents a BIM probabilistic
    information retrieval model.
    """
    def __init__(self, articles):
        """
        Initializes the model with the given articles.
        """
        self.articles=articles
        self.index= make_inverted_index(self.articles)
        self.df=doc_frequency(self.index)
        self.N=len(articles)
        self.query=[]
        self.u={}
        self.p={}
        self.term_weights={}
        self.rank={}


    def compute_term_weights(self):
        """
        Computes the term weights for each term in the inverted index
        based on the probabilities p and u, and saves them in a dictionary.
        """
        for term in self.index.keys():
            pi = self.p[term]
            ui = self.u[term]
            self.term_weights[term] = log(pi / (1 - pi)) + log((1 - ui) / ui)


    def vr_term(self, term, relevance):
        """
        Calculates the number of relevant documents containing the given term.
        """
        count=0
        for docid in relevance:
            if docid in self.index.get(term, set()):
                count += 1
        return count

    
    def update_p_u(self, relevance):
        """
        Updates the probabilities p and u for each term in the inverted index.
        """
        vr=len(relevance)
        for term in self.index.keys():
            vr_term=self.vr_term(term, relevance)
            self.p[term]=(vr_term + 0.5)/(vr + 1)
            self.u[term]=(self.df[term] - vr_term + 0.5)/(self.N - vr + 1)  
    

    def first_rsv_doc_query(self,docid): 
        """
        Calculates the RSV of a document for the first time,
        when p=0.5 and u=dfi/N.
        """
        c=0
        for term in self.query:
            if term in self.index and docid in self.index[term]:
                c+=inverse_doc_frequency_term(self.N, self.df[term])
        return c
        

    def rsv_doc_query(self,query, docid):
        """
        This method calculates the RSV of a document given a query.
        We preprocess the query by doing stemming and stopwords removal.
        """

        stops=set(stopwords.words('english'))
        # Add some words to the stopwords set
        stops.update(['isn', 'won', 're', 'll' ]) # s, t already in stopwords
        query=[word for word in query if word not in stops]
        self.query = set(stemming(query))

        if len(self.term_weights)==0:
            rsv_doc=self.first_rsv_doc_query(docid)
        else:
            rsv_doc=0
            for term in self.query:
                if term in self.index and docid in self.index[term]:
                    rsv_doc+=self.term_weights[term]
        return rsv_doc
    
    
    def answer_query(self, query):
        """
        Given a free-form text query or a query from the test
        collection, this method retrieves the articles according to
        the BIM model and it reutrns a list of tuples in which each
        tuple contains the docID and the RSV of that document.
        The list is ordered by descending RSV.
        """
        if type(query)==str:
            query=make_tokens(query)

        rank={}                 
        for i in range(self.N):
            rank[i]=self.rsv_doc_query(query,i)
        self.rank=sorted(rank.items(), key=lambda x:x[1], reverse=True)
        return self.rank


    def print_first_k_rel_docs(self,query,k=10):
        """
        This method prints the position, the docID, and the 
        RSV score of the k documents with highest RSV.
        """
        self.answer_query(query)
        for i in range(k):
            print(f"Position: {i+1}, Doc id: {self.rank[i][0]}, RSV score: {round(self.rank[i][1], 3)}")


    def relevance_feedback(self, query, relevance,n_print=10):
        """
        Given a query and the list docIDs relevant to the query,
        this method perform relevance feedback.
        """
        vr=len(relevance)
        rank=list(map(lambda x: x[0], self.answer_query(query)))
        rank=rank[0:vr]
        self.update_p_u(relevance)
        self.compute_term_weights()
        return self.print_first_k_rel_docs(query,n_print)
    

    def pseudo_relevance_feedback(self, query,k=5, n_print=10):
        """
        This method computes the pseudo relevance feedback
        by using the first k documents of answer query as relevant documents.
        """
        rank=list(map(lambda x: x[0], self.answer_query(query)))
        rank=rank[0:k]
        old_rank=[]
        count=0
        while rank!=old_rank and count<20: 
            old_rank=rank
            self.update_p_u(set(old_rank))
            self.compute_term_weights()
            rank=self.answer_query(query)
            rank=list(map(lambda x: x[0], rank))
            rank=rank[0:k]
            count+=1   
        return self.print_first_k_rel_docs(query, n_print)


    def precision_recall(self, query, relevance,k=10):
        """
        This method calculates the precision and the recall
        of the model given a query and a list of relevant documents.
        """
        self.answer_query(query)
        retrieved=set([self.rank[i][0] for i in range(k)])
        precision=len(retrieved.intersection(relevance))/len(retrieved)
        recall=len(retrieved.intersection(relevance))/len(relevance)
        print(f"The precision is: {round(precision,3)}, the recall is: {round(recall,3)}")
        
    
    def average_precision(self, query, relevance, k=10):
        """
        Given a query and the relevance documents to that query, this method 
        calculates the average precision of the first k retrieved documents.
        """
        self.answer_query(query)
        retrieved=[self.rank[i][0] for i in range(k)]
        precision_k=[len(relevance.intersection(set(retrieved[0:i+1])))/(i+1) for i in range(k)]
        rel_k=[1 if relevance.__contains__(self.rank[i][0]) else 0 for i in range(k)]
        gtp=sum(rel_k)
        pxr=[x*y for x,y in zip(precision_k, rel_k)]
        return gtp and (sum(pxr))/gtp or 0
    
    def mean_average_precision(self, elements, query_set, relevance_set, k=10):
        """
        This method calculates the mean average precision of the BIM model
        given the queries and the relative relevant documents.
        """
        queries=get_list(elements, query_set)
        relevance=get_list(elements, relevance_set)
        n=len(queries)
        map=0
        for i in range(n):
            map+=self.average_precision(queries[i],relevance[i],k)
        print(f"The mean average precision is: {round(map/n,3)}")

    
    def r_precision(self, query, relevance, to_print=True):
        """
        This method calculates the R-precision given a 
        query and the set of relevant documents.
        """
        self.answer_query(query)
        r=len(relevance)
        retrieved=set([self.rank[i][0] for i in range(r)])
        precision=len(retrieved.intersection(relevance))/len(retrieved)
        if to_print==True:
            print(f"The R-precision is: {round(precision,3)}")
        else:
            return precision


    def mean_r_precision(self, elements, query_set, relevance_set):
        """
        This method calculates the arithmetic mean of the R-precision values 
        for an information retrieval system over a set of n query topics.
        """
        queries=get_list(elements, query_set)
        relevance=get_list(elements, relevance_set)
        n=len(queries)
        r_precision=0
        for i in range(n):
            r_precision+=self.r_precision(queries[i],relevance[i], False)
        print(f"The mean R-precision is: {round(r_precision/n,3)}")



with open("data/preprocessed/articles.pkl", "rb") as f:
    articles = pickle.load(f)


bim=BIM_IRModel(articles)

with open("./index.pkl",'wb') as f:
    pickle.dump(bim,f)


