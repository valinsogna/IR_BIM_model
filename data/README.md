# Structure of dataset

* **`cran.all`**: the documents (1400) in the original format.
* **`cran.qry`**: the queries (225).
* **`cranqrel`**: the relevance assesments. They are in three columns:  $1^{st}$ query number, $2^{nd}$ the relevant document number, and the $3{rd}$ is the relevancy code.
* **`cranqrel_bin`**: the binary relevance assesments in TREC format. They are in four columns:  $1^{st}$ query number, $2^{nd}$ iteration (always zero), $3^{rd}$ the relevant document number, and the $4{th}$ is the relevancy code (0 or 1).
* **`readme`**: some attempt at explanation especially about the relevance judgements.

## Original format
Tags definitions :
- ***.I*** : Document unique number (identifier)
- ***.T*** : Document title
- ***.A*** : Document author(s)
- ***.B*** : Bibliography
- ***.W*** : Main document content (the article Abstract) -> **contains also the title!**

### Sample of original Cranfield document
```
.I 67
.T
dynamic stability of vehicles traversing ascending
or descending paths through the atmosphere .
.A
tobak and allen.
.B
naca tn.4275, 1958.
.W
dynamic stability of vehicles traversing ascending
or descending paths through the atmosphere .
an analysis is given of the oscillatory motions of vehicles which
traverse ascending and descending paths through the atmosphere at high
speed .  the specific case of a skip path is examined in detail, and
this leads to a form of solution for the oscillatory motion which should
recur over any trajectory .  the distinguishing feature of this form is
the appearance of the bessel rather than the trigonometric function as
the characteristic mode of oscillation .
```

## Query Relevance Judgment (*Qrels*)

In the original Cranfield collection, relevance judgments were made in 5 levels like follows :

| Relevance | Definition | Query/Docs <br>Match Count | % |
|:---:|---|:---:|:---:|
| -1 | References of no interest. | 225 | 12.2% |
| 1 | References of minimum interest, <br>for example, those that have been included from an historical viewpoint. | 128 | 7.0% |
| 2 | References which were useful, either as general background to the work <br>or as suggesting methods of tackling certain aspects of the work. | 387 | 21.1% |
| 3 | References of a high degree of relevance, the lack of which <br>either would have made the research impracticable <br>or would have resulted in a considerable amount of extra work. | 734 | 40.0% |
| 4 | References which are a complete answer to the question. | 363 | 19.8% |

:warning: This way of assessing relevance was aborted in TREC campaings as detailed in the following reference :
*Voorhees, Ellen M.* "The philosophy of information retrieval evaluation." Workshop of the cross-language evaluation forum for european languages. Springer, Berlin, Heidelberg, 2001.

Hence, we consider the new format of a Qrels file as follows: all initial relevancies having the scores **1, 2, 3, or 4** are considered as relevant (**all replaced with 1 value**) in the new formatted Cranfield collection. However, **-1 non relavant** initial assessments are **replaced with 0**.

The file `cranqrel_bin` is in TREC format of a Qrels file as follows:

| TOPIC | ITERATION | DOCNO | RELEVANCY |
|:---:|---|:---:|:---:|

Where :
 - **TOPIC** is the topic (query) number,
 - **ITERATION** is the feedback iteration (almost always zero and not used)
 - **DOCNO** is the official document number that corresponds to the "docno" field in the documents, and
 - **RELEVANCY** is a binary code of 0 for not relevant and 1 for relevant.

