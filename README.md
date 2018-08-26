# papers_collecting
Using python scraper to download all the NIPS and ICML papers from https://papers.nips.cc and http://proceedings.mlr.press

Usage for python 2:
To download NIPS papers, just execute: 
  python nips.py &
To download ICML papers, just execute: 
  python icml.py &

Modify the base.py to change the download configs:
such as on line 5-13: 
pkl_dir = 'pkl' 
papers_dir = 'papers' // The directory to download the papers. Paper from different conference will be saved into different sub-directory, such as papers/nips or papers/icml

paper_years = range(2013, 2018)
ip = '10.138.232.71'
