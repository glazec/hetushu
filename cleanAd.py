def cleanAd(text):
    ad = ['m.hetushu.com', 'www.hetushu.com',
          'wｗｗ.hetushu•ｃｏｍ', 'wwｗ•ｈｅtusｈu•cｏｍ', 'wwｗ•ｈｅtusｈu•cｏｍ', '和*图*书']
    for i in ad:
        text = text.replace('http://'+i, '')
        text = text.replace('http:// '+i, '')
        text = text.replace(i, '')
    text = text.replace('http://', '')
    return text

text=''
with open('textepub.txt', 'r', encoding='utf-8') as f:
    data = f.read()
    text = cleanAd(data)
    print(text)

with open('textepub.txt', 'w', encoding='utf-8') as f:
    f.write(text)
