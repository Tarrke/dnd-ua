#!/usr/bin/env python3
# coding: utf-8

"""
Simple downloader script to get the Unearthed Arcana PDF from WOTC
"""

import os
import urllib.request
import bs4 as bs
import io
import shutil

def download_file(url, file_name):
    """Download a file from an url an record it on the disk."""
    request = urllib.request.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11')
    with urllib.request.urlopen(request) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    return out_file

print('Hello World')

############################
# Main Configuration Section
base_url = "http://dnd.wizards.com"
main_url = base_url + "/articles-tags/unearthed-arcana"
# End of Section
############################

articles = []

has_next = True
next_url = main_url

while has_next:
    has_next = False
    download_file(next_url, 'index.html')

    html = open('index.html').read()
    soup = bs.BeautifulSoup(html, 'lxml')
    data = soup.find('li', attrs = {'class': 'pager-next'})
    print('data:', data)
    if data:
        print('This page has a follower')
        next_url = base_url + data.find('a')['href']
        print('Next URL:', next_url)
        has_next = True
    else:
        print('No more page to scan.')

    data = soup.find_all('article', attrs={'class':'article-preview'})
    for article in data:
        link = article.find('a', attrs={'class':'cta-button'})
        articles.append(base_url + link['href'])

if os.path.exists('index.html'):
    os.remove('index.html')

# Get a clean output directory
directory = 'output'
if not os.path.exists(directory):
    os.makedirs(directory)

for article in articles:
    print('Looking for pdf for article', article)
    if 'feature' in article:
        print('NOT LOOKING INTO', article)
        continue
    download_file(article, 'tmp.html')
    html2 = open('tmp.html').read()
    soup2 = bs.BeautifulSoup(html2, 'lxml')
    pdf_link = soup2.find('a', attrs={'class':'cta-button'})['href']
    pdf_tab = pdf_link.rsplit('/', 1)
    print(pdf_tab)
    pdf_name = pdf_tab.pop()
    if ' ' in pdf_name:
        pdf_tab.append(urllib.parse.quote(pdf_name))
    else:
        pdf_tab.append(pdf_name)
    print(pdf_tab)
    pdf_link = '/'.join(pdf_tab)
    pdf_name = os.path.join(directory, pdf_tab[-1].replace('%20','_'))
    if not os.path.exists(pdf_name):
        print('Downloading pdf', pdf_link, 'as', pdf_name)
        download_file(pdf_link, pdf_name)

# Cleaning current directory from temp files
if os.path.exists('tmp.html'):
    os.remove('tmp.html')

# print(articles)
# print(data)
