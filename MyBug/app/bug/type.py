#coding=utf-8
from bs4 import BeautifulSoup
import urllib

from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'I Love C++!',
    'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://root:041166@localhost:3306/myserver',
    'SQLALCHEMY_COMMIT_ON_TEARDOW': True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': True
})

db = SQLAlchemy(app)
Base=db.Model

#用于存储一些食物分类

class Type(Base):
    __tablename__='Type'
    
    ID=db.Column(db.Integer,primary_key=True)
    Item=db.Column(db.String(100),nullable=True)
    Name=db.Column(db.String(100),nullable=True)
    Url=db.Column(db.String(200),nullable=True)
    Img=db.Column(db.String(200))
    TypeItem = db.relationship('TypeItem', backref='Type', lazy='dynamic')


class TypeItem(Base):
    __tablename__='typeitem'
    
    ID=db.Column(db.Integer,primary_key=True)
    typeID=db.Column(db.Integer,db.ForeignKey(Type.ID))
    Url=db.Column(db.String(200))
    Name=db.Column(db.String(200))
    Img=db.Column(db.String(200))
    Introduction=db.Column(db.String(200))
    Virtue=db.Column(db.String(200))
    Taboo=db.Column(db.String(200))

soup=BeautifulSoup(urllib.urlopen('http://food.ttys5.com/index/food_list/2'),"lxml")
subsoup=soup.find(id="anothercontent1")
h=subsoup.find('h2')
for tag in subsoup.find_all('p'):
    text=h.get_text()
    for item in tag.find_all('a'):
        href=item.get('href')
        name=item.get('title')
        type=Type(Item=text,Url=href,Name=name)
        db.session.add(type)
    h=h.find_next('h2')
     
if __name__=='__main__':
    db.session.commit()
    
        
    
