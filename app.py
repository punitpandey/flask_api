from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app=Flask(__name__)
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'flask.sqlite')
db=SQLAlchemy(app)
ma=Marshmallow(app)

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(80))
    email=db.Column(db.String(120))
    def __init__(self,username,email):
        self.username=username
        self.email=email

class UserSchema(ma.Schema):
    class Meta:
        fields=('username','email')
user_schema=UserSchema()
users_schema=UserSchema(many=True)


@app.route('/')
def flaskApp():
    return "Hello world"

@app.route('/user',methods=['GET'])
def getAllUser():
    all_users=User.query.all()
    result=users_schema.dump(all_users)
    return jsonify(result)

@app.route('/user',methods=['PUT'])
def addUser():
    username=request.json['username']
    email=request.json['email']
    new_user=User(username,email)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

@app.route('/user/<id>',methods=['PUT'])
def updateUser(id):
    user=User.query.get(id)
    user.username=request.json['username']
    user.email=request.json['email']
    db.session.commit()
    return user_schema.jsonify(user)

@app.route('/user/<id>',methods=['GET'])
def getUser(id):
    user=User.query.get(id)
    return user_schema.jsonify(user)

@app.route('/user/<id>',methods=['DELETE'])
def delUser(id):
    user=User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

if __name__=='__main__':
    db.create_all()
    app.run(debug=True)