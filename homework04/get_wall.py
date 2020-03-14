import requests
import config
from gensim import corpora, models
from pymorphy2 import *
import gensim

def get():
    code = """return API.wall.get({
        "owner_id": -186208472,
        "domain": "itmoru",
        "offset": 0,
        "count": 10,
        "filter": "all",
        "extended": 0,
        "fields": "",
        "v": "5.103"
    });"""

    response = requests.post(
        url="https://api.vk.com/method/execute",
            data={
                "code": code,
                "access_token": 'cbb4b0a186e0b7592b8312112338813f42b7358c19c230bd7f2d67a0767a98a996b091252500bb1ea6863',
                "v": "5.103"
            }
    )
    response = response.json()
    return response
def change_text(text):
    list_word = []
    symbols = ['!', '@', '#', '$', '^', '&', '?', '.', ',', '(', ')', '*', ':', ';', '№', '-', '=', '+', '_', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    for i in range(10):
        p = text['response']['items'][i]['text'].split('\n')
        k = ' '.join(map(str, p))
        while k.find('http') != -1:
            o = k.find('http')
            g = k.find(' ', o + 1)
            k = k[:o] + k[g + 1:]
        for j in symbols:
            if j in k:
                p = k.split(j)
                k = ' '.join(map(str, p))
        p = ' '.join(map(str, p))
        k = p.split(' ')
        list_word += [k]

    h = ['NUMR', 'ADVB', 'NPRO', 'PRED', 'PREP', 'CONJ', 'PRCL', 'INTJ']
    morph = MorphAnalyzer()
    list_end = []
    for i in range(len(list_word)):
        list_end +=[[]]
        for j in range(len(list_word[i])):
            l = morph.parse(list_word[i][j])[0].tag.POS
            if l not in h and len(list_word[i][j]) > 2 and list_word[i][j] != '':
                list_end[i].append(morph.parse(list_word[i][j])[0].normal_form)
    return list_end

common_texts = change_text(get())

common_dictionary = corpora.Dictionary(common_texts)
common_corpus = [common_dictionary.doc2bow(text) for text in common_texts]
lda_model = gensim.models.ldamodel.LdaModel(corpus=common_corpus,
                                           id2word=common_dictionary,
                                           num_topics=4,
                                           random_state=100,
                                           update_every=1,
                                           chunksize=10,
                                           passes=10,
                                           alpha='symmetric',
                                           iterations=100,
                                           per_word_topics=True)

print(lda_model.print_topics())
