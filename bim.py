from math import log 
import pickle
from utils.functions import *

class BIM():
    """
    In this section we create a class for the BIM probabilistic
    information retrieval model. This class contains the attributes 
    and the methods for the BIM model.
    """
    def __init__(self, articles):
        """
        The class contains the following attributes:
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
        This method computes the term-weight for each term 
        in the inverted index and save them in a dictionary
        in which the keys are the terms of the inverted index
        and the values are the term-weights.
        """
        for term in self.index.keys():
            pi=self.p[term]
            ui=self.u[term]
            self.term_weights[term]=log(pi/(1-pi))+log((1-ui)/ui)


    def vr_term(self, term, relevance):
        """
        This method calculates the number of relevant documents 
        containing the term that has been given as input.
        """
        count=0
        for docid in relevance:
            if self.index[term].__contains__(docid):
                count+=1
        return count

    
    def update_p_u(self, relevance):
        """
        This method updates the values of the probabilities
        p and u for each  term in the inverted index. 
        """
        vr=len(relevance)
        for term in self.index.keys():
            vr_term=self.vr_term(term, relevance)
            self.p[term]=(vr_term + 0.5)/(vr + 1)
            self.u[term]=(self.df[term] - vr_term + 0.5)/(self.N - vr + 1)  
    

    def first_rsv_doc_query(self,docid): 
        """
        This method calculates the RSV of a document.
        It is used to calculate the RSV for the first time,
        when we set p=0.5 and u=dfi/N. Indeed in this case,
        the RSV is estimated to be sum of the inverse document 
        frequency for each term present in both the query and article.
        """
        c=0
        for term in self.query:
            if self.index.__contains__(term) and self.index[term].__contains__(docid):
                c+=inverse_doc_frequency_term(self.N, self.df[term])
        return c
        

    def rsv_doc_query(self,query, docid):
        """
        This method calculates the RSV of a document given a query.
        We preprocess the query by doing stemming before 
        calculating the RSV.
        """
        self.query=set(stemming(query))

        if len(self.term_weights)==0:
            rsv_doc=self.first_rsv_doc_query(docid)
        else:
            rsv_doc=0
            for term in self.query:
                if self.index.__contains__(term) and self.index[term].__contains__(docid):
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
            query=make_list_query(query)

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

    
    def r_precision(self, query, relevance):
        """
        This method calculates the R-precision given a 
        query and the set of relevant documents.
        """
        self.answer_query(query)
        r=len(relevance)
        retrieved=set([self.rank[i][0] for i in range(r)])
        precision=len(retrieved.intersection(relevance))/len(retrieved)
        print(f"The R-precision is: {round(precision,3)}")



with open("data/preprocessed/articles.pkl", "rb") as f:
    articles = pickle.load(f)

bim=BIM(articles)

with open("./index.pkl",'wb') as f:
    pickle.dump(bim,f)


