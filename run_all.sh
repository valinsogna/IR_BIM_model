#! /bin/bash

cd data/preprocessed
python3 import.py
cd ../..
python3 bim.py