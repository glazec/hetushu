# -*- coding:UTF-8 -*-
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def clean_ad(text_bf):
    # <q>,<tt>,<var>
    # ad = ['m.hetushu.com', 'www.hetushu.com',
    #       'wｗｗ.hetushu•ｃｏｍ', 'wwｗ•ｈｅtusｈu•cｏｍ', 'wwｗ•ｈｅtusｈu•cｏｍ']
    # for i in ad:
    #     text = text.replace('http://'+i, '')
    #     text = text.replace('http:// '+i, '')
    #     text = text.replace(i, '')
    # text=text.replace('http://','')
    def get_only_text(elem):
        for item in elem.children:
            if isinstance(item,bs4.element.NavigableString):
                yield item
    clean_text = []
    for i in text_bf:
        clean_text.append(''.join(get_only_text(i)))
        print(''.join(get_only_text(i)))
    return clean_text

def scrap(url,context):
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    html = driver.page_source
    driver.close()
    bf = BeautifulSoup(html, features="lxml")
    content = bf.find('div', id='content')
    content_bf = BeautifulSoup(str(content.contents), features="lxml")
    chapter = content_bf.find('h2', {"class": "h2"}).text
    volume = content_bf.find('h2').text
    raw_text = content_bf.findAll('div')
    clean_text= clean_ad(raw_text)
    # print(clean_text)
    text = '\n'.join(clean_text)
    print(volume)
    print(chapter)
    with open('textepub.txt', 'a+', encoding="utf-8") as f:
        if context==volume:
            f.write('\n\n'+chapter+'\n\n'+text)
        else:
            f.write('\n\n'+volume+'\n'+chapter+'\n\n'+text)
    context = volume
    return context

# get chapters url
demo_html=''
with open('demo.html', 'r', encoding="utf-8") as f:
    demo_html=f.read()
bf_demo_html = BeautifulSoup(demo_html, features="lxml")
chapters = bf_demo_html.findAll('dd')
chapters_url = [i.findChildren('a')[0]['href'] for i in chapters]

with open('chapters.txt', 'w', encoding="utf-8") as f:
    f.write(str(chapters))

# print(chapters_url)
context = ''
for i in chapters_url[737:]:
    context=scrap(i,context)
