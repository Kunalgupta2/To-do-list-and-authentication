from flask import Flask, render_template, request,redirect,session
from functools import wraps
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app=Flask(__name__)
bcrypt=Bcrypt(app)
app.secret_key="Awaii"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///todo.db"
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///task.db"
db=SQLAlchemy(app)
class Login(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(40), nullable=False)
    email_id=db.Column(db.String(100), nullable=False)
    password=db.Column(db.String(100), nullable=False)

class Newuser(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    email_id=db.Column(db.String(100), nullable=False)
    username=db.Column(db.String(40), nullable=False)
    password=db.Column(db.String(100), nullable=False)
class Tasks(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    newtask=db.Column(db.String(100), nullable=False)
    date=db.Column(db.DateTime)
    


    

@app.route("/")
def home():

    return redirect("/login")


def logged_in(route):
    def check(*args,**kwargs):
        if session.get("login"):
            return route(*args,**kwargs)
        else:
            return redirect("/")
    return check



@app.route("/dashboard")
def dash():
    return "Already Logged in, either use /print or  use /logout"

@app.route("/login", methods=['POST','GET'])
def login():
    if session.get("login"):
        return redirect("/dashboard")
    if request.method=='POST':
        Email_id=request.form.get("email_id")
        Password=request.form.get("password")
        user=Newuser.query.filter_by(email_id=Email_id ).first()
        if user:
            is_validate =bcrypt.check_password_hash(user.password,   Password)
            if is_validate==True:
                session["login"]=True
                return redirect("/taskadd")
            else:
                return "invalid pass "
        else:
            return "invalid user"
    else:
        return render_template("index.html")

        
    
        

@app.route("/logout")
def logout():
    session["login"]=False  
    return redirect("/")  

@app.route("/signup")
def sign():
    return render_template("newuser_login.html")

@app.route("/signupp", methods=["POST","GET"])
def signup():
    if request.method=="POST":
        name=request.form.get("name")
        username=request.form.get("username")
        
            

        email_id=request.form.get("email_id")
        password=request.form.get("password")
        user=Newuser.query.filter_by(username=username).first()
        
        if user:
            return "username already exist, enter new username"

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        
        if not name:
            return "Name cannot be empty"
        signup1=Newuser(name=name, email_id=email_id,username=username, password=hashed_password)
        db.session.add(signup1)
        db.session.commit()
        return render_template("index.html")
    return render_template("newuser_login.html")
    
    # else:
    #     return render_template("newuser_login.html")
@app.route("/print")
@logged_in
def print2():
    data=Newuser.query.all()
    return render_template("table.html",logins=data)

@app.route("/deleteacc/<int:id>/")
def delacc(id):
    data=Newuser.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect("/print")

#to do functions
@app.route('/taskadd')
def hom():
    task2=Tasks.query.all() 
    return render_template("list.html",data=task2)
@app.route("/add")
def addtask():
    return render_template("index2.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method=="POST":
        newtask=request.form["new task"]
        date_str=request.form["date"]
        date=datetime.strptime(date_str,"%Y-%m-%d")
        task1=Tasks(newtask=newtask, date=date)
        db.session.add(task1)
        db.session.commit()

        
    
        return redirect("/taskadd")
    
@app.route("/remove/<int:id>/")
def remove(id):
    data=Tasks.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect("/")
@app.route("/update/<int:id>/", methods=['POST','GET'])
def update(id):
    task = Tasks.query.get(id)
    if request.method == 'POST':
        newtask = request.form['new task']
        date_str=request.form["date"]
        date=datetime.strptime(date_str,"%Y-%m-%d")
        
        if newtask:
            task.newtask = newtask
            task.date=date
            db.session.commit()
            return redirect('/taskadd')
        else:
            return 'Task cannot be empty'
    else:
        return render_template('update_task.html', task=task,id=id)





if __name__=="__main__":
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)




    
