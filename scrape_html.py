from urllib.request import urlopen
from bs4 import BeautifulSoup
import mechanicalsoup as ms
from nltk.corpus import words
import random
import csv
from tqdm import trange
import sys


def clean(soup):
  for link in soup("link"):link.decompose()
  for meta in soup("meta"):meta.decompose()
  for head in soup("head"):head.decompose()
  for script in soup("script"):soup.script.extract()
  for style in soup("style"):style.decompose()
  for path in soup("path"):path.decompose()
  for img in soup("img"):img.decompose()
  REMOVE_ATTRIBUTES = ['lang','language','onmouseover','onclick','id','onblur','onload','onmouseout','script','dir','face','class','hspace','text','data-spy','data-bind','data-testid']


  for attr_del in REMOVE_ATTRIBUTES:[s.attrs.pop(attr_del) for s in soup.find_all() if attr_del in s.attrs]

  return soup

def remove_non_ascii(s):
    return "".join(c for c in s if ord(c)<128)


def extract_html(name,no):
  count=0


  browser=ms.StatefulBrowser(user_agent="MechanicalSoup")
  urls=[]  
  while True:

    n=random.randint(0,236736)
    word=words.words()[n]


    browser.open("https://duckduckgo.com/")
    browser.select_form('#search_form_homepage')
    browser['q']=word
    browser.submit_selected()


    for n,i in enumerate(browser.page.select('a.result__a')):
  
      content=[]
      url=i.attrs['href']
      if url in urls:continue
      urls.append(url)


      try:
          page = urlopen(url,timeout=15).read().decode(encoding="iso-8859-1")
      except:
          continue

      soup = clean(BeautifulSoup(page, 'html.parser'))
         

      for tags in soup.find_all():
        for i in tags.contents:
          if '\n' not in i and isinstance(i,str):tags.contents[tags.contents.index(i)].replace_with(' [MASk] ')
      soup=str(soup)
      text=remove_non_ascii(soup.replace('\n','').replace('\r','').replace('\t','').replace(' [MASk]  [MASk]','[MASK]') +'\n')#+'\n\n<|endoftext|>\n\n'
      for  i in range(len(text)):
        if text[i]=='>' and ord(text[i-1])>32 and ord(text[i-1]) <128:
          text=text[:i+1] + ' ' + text[i+1:]
        if text[i]=='<' and ord(text[i-1])>32 and ord(text[i-1]) <128 and i is not 0:
          text=text[:i] + ' ' + text[i:]
      text=" ".join(text.split()) +'\n'
      count+=1
          
             
      with open(f'{name}', 'a') as f:
         f.write(text)
         f.close()
      if count%10==0:print(count)
      while count==no:sys.exit(0)i

extract_html('html.txt',1000)
