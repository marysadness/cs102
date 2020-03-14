from bottle import (
    route, run, template, request, redirect
)

from db import News, session
from scraputils import get_news
from bayes import NaiveBayesClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy.orm import load_only

@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()#список объектов
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    label = request.query.label
    new_id = request.query.id
    news = s.query(News).filter(News.id == new_id).one()
    news.label = label
    s.commit()
    redirect("/news")

from scraputils import get_news
@route("/update")
def update_news():
    s = session()
    news = []
    pages = get_news("https://news.ycombinator.com/newest", 3)
    old_new = s.query(News).all()
    old_list = [(old.author, old.title) for old in old_new]
    for new in pages:
        if (new['author'] not in old_list) and (new['title'] not in old_list):
            news.append(News(title=new['title'],
                             author=new['author'],
                             url=new['url'],
                             comments=new['comments'],
                             points=new['points']))
        print(new)
    s.bulk_save_objects(news)
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    classifier = NaiveBayesClassifier()
    train_news = s.query(News).filter(News.label != None).options(load_only("title", "label")).all()
    x_train = [row.title for row in train_news]
    y_train = [row.label for row in train_news]
    print(len(x_train))

    classifier.fit(x_train, y_train)
    test_news = s.query(News).filter(News.label == None).all()
    x = [row.title for row in test_news]
    labels = classifier.predict(x)
    good = [test_news[i] for i in range(len(test_news)) if labels[i] == 'good']
    maybe = [test_news[i] for i in range(len(test_news)) if labels[i] == 'maybe']
    never = [test_news[i] for i in range(len(test_news)) if labels[i] == 'never']
    rows = [good] + [maybe] + [never]
    return template('news_recommended', rows=rows, label=['Good', 'Maybe', 'Never'])


if __name__ == "__main__":

    s = session()
    train_news = s.query(News).filter(News.label != None).options(load_only("title", "label")).all()
    x_train = [row.title for row in train_news]
    y_train = [row.label for row in train_news]
    print(len(x_train))
    X_train, Y_train, X_test, y_test = x_train[:700], y_train[:700], x_train[700:], y_train[700:]
    model =  Pipeline([
        ('vectorizer', TfidfVectorizer()),
        ('classifier', MultinomialNB(alpha=0.5)),
    ])
    model.fit(X_train, Y_train)
    print(model.score(X_test, y_test))
    model = NaiveBayesClassifier()
    model.fit(X_train, Y_train)

    print(model.score(X_test, y_test))
    run(host="localhost", port=8080)
#add many- bulk_save_objects(object)
#/- разные маршруты

