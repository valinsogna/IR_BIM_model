# Structure of dataset

* ***cran.all***: the documents (1400) in the original format.
* ***cran.qry***: the queries (225).
* ***cranqrel***: the relevance assesments. They are in three columns:  $1^{st}$ query number, $2^{nd}$ the relevant document number, and the $3{rd}$ is the relevancy code.
* ***readme***: some attempt at explanation especially about the relevance judgements.

## Original format
Tags definitions :
- ***.I*** : Document unique number (identifier)
- ***.T*** : Document title
- ***.A*** : Document author(s)
- ***.B*** : Bibliography
- ***.W*** : Main document content (the article Abstract) -> contains also the title!

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