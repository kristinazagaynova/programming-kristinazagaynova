from bottle import (
    route, run, template, request, redirect
)

from scrapper import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    sess = session()
    rows = sess.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    lbl = request.query["label"]
    id1 = request.query["id"]
    session = session()
    sess = session.query(News).get(id1)
    sess.lbl = lbl
    session.add(s)
    session.commit()
    redirect("/news")


@route("/update")
def update_news():
    session = session()
    link = get_news("https://news.ycombinator.com/newest", 1)
    for i in range(len(link)):
        a = News(title=link[i]["title"], author=author[i]["author"],
                 comments=link[i]["comments"], points=link[i]["points"],
                 url=link[i]["url"])
        if (session.query(News).filter(News.tittle == a.title and News.author==a.author).count()) == 0:
            session.add(a)
    session.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    sess = session()
    unclassified: tp.List[tp.Tuple[int, str]] = [
        (i.id, stemmer.clear(i.title))
        for i in sess.query(News).filter(News.label == None).all()
    ]
    x1 = [i[1] for i in unclassified]
    if not pathlib.Path(
            f"{os.path.dirname(os.path.realpath(__file__))}/../model/model.pickle"
    ).is_file():
        raise ValueError(
            "Classifier is untrained! Please mark enough news to adequately train the model and run bayes.py to save it."
        )
    with open(
            f"{os.path.dirname(os.path.realpath(__file__))}/../model/model.pickle", "rb"
    ) as model_file:
        model = NaiveBayesClassifier(alpha=0.1)
        model = pickle.load(model_file)
    labels = model.predict(x1)
    for i, e in enumerate(unclassified):
        extract = sess.query(News).filter(News.id == e[0]).first()
        extract.label = labels[i]
        sess.commit()
    rows = sess.query(News).filter(News.label != None).order_by(News.label).all()

    return template("classified_template.tpl", rows=rows)


if __name__ == "__main__":
    run(host="localhost", port=8080)

