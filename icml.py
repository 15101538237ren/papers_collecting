#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urlparse, pickle, os, urllib,re
import numpy as np
from base import *
from BeautifulSoup import BeautifulSoup
nips_url = "http://proceedings.mlr.press"

content_dict = {str(year) : {} for year in paper_years}
paper_collection_name = 'icml'
ret_content = request_url(paper_collection_name, nips_url)
soup_main = BeautifulSoup(ret_content)
lis = soup_main('li')
pickle_fp = os.path.join(pkl_dir, paper_collection_name + '.pkl')
paper_dirname = paper_collection_name
lis = lis[12 : 59]
pattern = u'abstract\s*=\s*{([^{]+)}'
re_pattern = re.compile(pattern)
print re_pattern.findall(u'abstract = {aaa}')

for li in lis:
    for key in content_dict.keys():
        if li.text.find(key) >=0 and li.text.find('ICML') >=0:
            paper_of_year_dir = os.path.join(papers_dir,paper_dirname,key)
            if not os.path.exists(paper_of_year_dir):
                os.makedirs(paper_of_year_dir)
            conference_papers_href = urlparse.urljoin(nips_url,li.a['href'])
            content_dict[key]['url'] = conference_papers_href
            content_dict[key]['papers'] = []
            soup_papers = BeautifulSoup(request_url(paper_collection_name,conference_papers_href))
            divs_of_papers = soup_papers('div')[5:-2]
            for div in divs_of_papers:
                paper_dict = {}
                div_contents = div.contents[1:6:4]
                paper_dict['title'] = div_contents[0].text
                links_content = div_contents[1]
                abs_url = links_content.contents[1]['href']
                paper_download_url = links_content.contents[3]['href']
                paper_dict['url'] = paper_download_url
                paper_title = paper_dict['title'].lower().replace(" ", "_")
                paper_title = re.sub('[^a-z0-9_]+', '', paper_title)
                print paper_title
                urllib.urlretrieve(paper_dict['url'], os.path.join(paper_of_year_dir, paper_title + '.pdf'))
                if len(links_content)>= 5:
                    paper_supplement_url = links_content.contents[5]['href']
                    paper_dict['sup_url'] = paper_supplement_url
                abstract_div = BeautifulSoup(request_url(paper_collection_name,urlparse.urljoin(nips_url, abs_url))).text
                abstract_div = re.sub(u'<[^>]*>', u'', abstract_div)
                abstract = ""
                start_pos = abstract_div.find('%X ')
                end_pos = abstract_div.find('Copy Endnote')
                paper_dict['abstract'] = abstract_div[start_pos + 3:end_pos]
                content_dict[key]['papers'].append(paper_dict)
#
with open(pickle_fp, 'wb') as pickle_file:
    pickle.dump(content_dict, pickle_file, -1)
    print "dump %s sucessful" % pickle_fp

if __name__ == "__main__":
    pass