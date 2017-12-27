#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urlparse, pickle, os, urllib
from base import *
from BeautifulSoup import BeautifulSoup
nips_url = "https://papers.nips.cc"

content_dict = {str(year) : {} for year in paper_years}
soup_main = BeautifulSoup(request_url(nips_url))
links = soup_main('a')

pickle_fp = os.path.join(pkl_dir,'nips.pkl')
nips_dirname = 'nips'

for link in links:
    for key in content_dict.keys():
        if link.text.find(key) >=0:
            print key
            paper_of_year_dir = os.path.join(papers_dir,nips_dirname,key)
            if not os.path.exists(paper_of_year_dir):
                os.makedirs(paper_of_year_dir)
            conference_papers_href = urlparse.urljoin(nips_url,link['href'])
            content_dict[key]['url'] = conference_papers_href
            content_dict[key]['papers'] = []
            soup_papers = BeautifulSoup(request_url(conference_papers_href))
            links_of_papers = soup_papers('a')
            links_of_papers = links_of_papers[9:-1]
            for link_of_paper in links_of_papers:
                href_of_paper = link_of_paper['href']
                filename_of_paper = href_of_paper.split('/')[-1]
                if href_of_paper.find('paper') >= 0:
                    print filename_of_paper
                    paper_dict = {}
                    paper_dict['title'] = link_of_paper.text
                    paper_soup = BeautifulSoup(request_url(urlparse.urljoin(nips_url, href_of_paper)))
                    links_of_this_paper_page = paper_soup('a')
                    for link_otp in links_of_this_paper_page:
                        if link_otp.text == "[PDF]":
                            paper_url = urlparse.urljoin(nips_url, link_otp['href'])
                            paper_dict['url'] = paper_url
                            break
                    p_of_this_paper = paper_soup('p')
                    for p_otp in p_of_this_paper:
                        if len(p_otp.attrs):
                            paper_dict['abstract'] = p_otp.text
                            break
                    content_dict[key]['papers'].append(paper_dict)
                    urllib.urlretrieve(paper_dict['url'],os.path.join(paper_of_year_dir,filename_of_paper + '.pdf'))
with open(pickle_fp, 'wb') as pickle_file:
    pickle.dump(content_dict, pickle_file, -1)
    print "dump %s sucessful" % pickle_fp

if __name__ == "__main__":
    pass