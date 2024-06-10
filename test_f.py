from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from sqlalchemy import Integer, String, Text, DateTime
from flask_msearch import Search


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(app, model_class=Base)


class User(db.Model):
    id = db.Column(Integer, primary_key=True)
    title = db.Column(String(100), nullable=False)
    intro = db.Column(String(300), nullable=False)
    text = db.Column(Text, nullable=False)
    date = db.Column(DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template("test_f1.html")


@app.route('/about_site.html')
def about_site():
    return render_template("about_site.html")


@app.route('/test_f1_enter.html')
def test_f1_enter():
    return render_template("test_f1_enter.html")


@app.route('/test_f1.html')
def back_from_enter():
    return render_template("test_f1.html")


@app.route('/test_f1_registration.html')
def test_f1_registration():
    return render_template("test_f1_registration.html")


@app.route("/posts.html")
def posts():
    articles = User.query.order_by(User.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route("/posts/<int:id>")
def post_detail(id):
    article = User.query.get_or_404(id)
    return render_template("post_detail.html", article=article)


@app.route("/posts/<int:id>/del")
def post_delete(id):
    article = User.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts.html')
    except:
        return "При удалинии статьи произошла ошибка"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = User.query.get_or_404(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts.html')
        except Exception as e:
            return "При редактировании статьи произошла ошибка", e
    else:
        return render_template("post_update.html", article=article)


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_comment(id):
    article = User.query.get_or_404(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts.html')
        except Exception as e:
            return "При редактировании статьи произошла ошибка", e
    else:
        return render_template("post_update.html", article=article)


@app.route('/create_article.html', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = User(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts.html')
        except Exception as e:
            return "При добавлении статьи произошла ошибка", e
    else:
        return render_template("create_article.html")


if __name__ == "__main__":
    app.run(debug=True)
