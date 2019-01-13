from flask import Flask,render_template,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from forms import NewsForm
from datetime import datetime

app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////sqlite/database.sqlite'
app.config['SECRET_KEY'] = 'a rabdom string'
db = SQLAlchemy(app)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    image = db.Column(db.String(300),)
    author = db.Column(db.String(20),)
    view_count =db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    is_valid =db.Column(db.Boolean)

    def __repr__(self):
        return '<News %r>'% self.title

@app.route('/')
def index():
    news_list = News.query.filter_by(is_valid=1)
    return render_template('index.html',news_list=news_list)

@app.route('/cat/<name>/')
def cat(name):
    """カテゴリー"""
    news_list = News.query.filter(News.type == name)
    return render_template('cat.html', name=name,news_list=news_list)

@app.route('/detail/<int:pk>/')
def detail(pk):
    """詳細"""
    new_obj = News.query.get(pk)
    return render_template('detail.html', pk=pk, new_obj=new_obj)

@app.route('/admin/')
@app.route('/admin/<int:page>/')
def admin(page=None):
    if page is None:
        page = 1
    page_data = News.query.paginate(page=page, per_page=5)
    return render_template('admin/index.html', page_data=page_data)

@app.route('/admin/update/<int:pk>/',methods=('GET','POST'))
def update(pk):
    new_obj = News.query.get(pk)
    if not new_obj:
        return redirect(url_for('admin'))
    form = NewsForm(obj=new_obj)
    if form.validate_on_submit():
        new_obj.title = form.title.data
        new_obj.content = form.content.data
        new_obj.is_valid = int(form.is_valid.data)
        new_obj.created_at = datetime.now()
        new_obj.image = form.image.data
        new_obj.type = form.type.data
        db.session.add(new_obj)
        db.session.commit()
        flash('修正しました','ok')
        return redirect(url_for('admin'))
    return render_template('admin/update.html', form=form)

@app.route('/admin/delete/<int:pk>/',methods=('GET','POST'))
def delete(pk):
    new_obj = News.query.get(pk)
    if not new_obj:
        return redirect(url_for('admin'))


@app.route('/admin/add/',methods=('GET','POST'))
def add():
    form = NewsForm()
    if form.validate_on_submit():
        new_obj = News(
            title=form.title.data,
            content=form.content.data,
            type=form.type.data,
            image=form.image.data,
            created_at=datetime.now()
        )
        db.session.add(new_obj)
        db.session.commit()
        flash('追加しました', 'ok')
        return redirect(url_for('admin'))
    return render_template('admin/add.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)