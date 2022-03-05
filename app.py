from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

TOP_LEVEL_DIR = os.path.abspath(os.curdir)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = TOP_LEVEL_DIR + '/static/'
db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.id}'

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'name': self.name,
            'description': self.description,
            'image': self.image,
            'date': self.date,
        }


@app.route("/")
def blog_list():
    all_blog = Blog.query.all()
    return render_template('list.html', all_blog=all_blog)


@app.route("/add_blog/", methods=['GET', 'POST'])
def add_blog():
    if request.method == 'POST':
        title = request.form['title']
        name = request.form['name']
        description = request.form['description']
        image = request.files['image']
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], str(image.filename)))
        path = '/static/' + str(image.filename)
        blog = Blog(title=title, name=name, description=description, image=path)
        db.session.add(blog)
        db.session.commit()
        return redirect('/')
    return render_template('add_blog.html')


@app.route("/update_blog/<int:id>/", methods=['GET', 'POST'])
def update_blog(id):
    if request.method == "POST":
        title = request.form['title']
        name = request.form['name']
        description = request.form['description']
        image = request.files['image']
        image.save(image.filename)
        blog = Blog.query.filter_by(id=id).first()
        blog.title = title
        blog.name = name
        blog.description = description
        blog.image = image.name
        db.session.add(blog)
        db.session.commit()
        return redirect('/')
    blog_update = Blog.query.filter_by(id=id).first()
    return render_template('update_blog.html', blog_update=blog_update)


@app.route("/delete_blog/<int:id>/")
def delete_blog(id):
    blog_delete = Blog.query.filter_by(id=id).first()
    db.session.delete(blog_delete)
    db.session.commit()
    return redirect('/')
