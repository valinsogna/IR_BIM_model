# IR system: BIM model
Implementation in Python of BIM, a probabilistic model for IR, able to:

- answer free-form text queries.
- allow relevance feedback.
- allow use of pseudo-relevance feedback.

Evaluation of the effectiveness of the system is performed on a set of test queries by:
- precision/recall for a query.
- mean average precision for a set of queries.
- R-precision of the top R ranked documents for a query.

## Dataset used

The dataset used is the [Cranfield](http://ir.dcs.gla.ac.uk/resources/test_collections/cran/) which is a standard Information Retrieval text collection, consisting of 1400 documents (1.6 MB) from the aerodynamics field, in SGLM format. 
The collection contains 225 queries with relevance feedback.

