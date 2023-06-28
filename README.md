# IR system: BIM model
Implementation in Python of BIM, a probabilistic model for IR, able to:

- answer free-form text queries.
- allow relevance feedback.
- allow use of pseudo-relevance feedback.

Evaluation of the effectiveness of the system is performed on a set of test queries by:
- precision/recall for a query.
- mean average precision for a set of queries.
- R-precision of the top R ranked documents for a query.
- mean average R-precision for a set of queries.

## Dataset

The dataset used is the [Cranfield](http://ir.dcs.gla.ac.uk/resources/test_collections/cran/) which is a standard Information Retrieval text collection, consisting of 1400 documents (1.6 MB) from the aerodynamics field, in SGLM format. 
The collection contains 225 queries with relevance feedback.

## Structure

The project is structured as follows:
- `data` folder contains the dataset in original and preprocessed form.
- `utils` folder contains the file `function.py` with the functions used in the project.
- `bim.py` contains the implementation of the model bim.
- `index.pkl` is the index built by the model bim in pickle format.
- `run_all` bash script to run the entire project.
- `test_model.ipynb` jupyter notebook to test the model.

## Run

To import the dataset, preprocessing it and build the index, simply execute the bash script `run_all`:
```bash 
bash run_all.sh
```

## Results

To see the performance and usage of the index built, run the juptyer notebook `test_model.ipynb`:


## Python Packages

- [NLTK](https://www.nltk.org/) for text processing.
- [NumPy](https://numpy.org/) for numerical operations.

 **Warning**
 To run bash script `run_all` enable downlaod of nltk packages in `utils/functions.py` file at line 6,7:
 ```Python
 nltk.download('stopwords')
 nltk.download('punkt')
 ```
