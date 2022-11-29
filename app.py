from flask import Flask,render_template,request,abort,redirect,url_for
from flask_admin import Admin,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_login import UserMixin,LoginManager,current_user,login_user
from flask import session
import mysql.connector
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField
from flask_bootstrap import Bootstrap


app = Flask(__name__)
admin=Admin(app)
Bootstrap(app);


app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/test"
app.config['SECRET_KEY'] = 'mysecret'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test'

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test"
  )



db= SQLAlchemy(app);  
mysql=MySQL(app);

login=LoginManager(app);


@login.user_loader
def userid(id):
    return user.query.get(int(id))
    


#Classes

class user(FlaskForm):
    
    Username=db.Column(db.Text, unique=True)
    Password=db.Column(db.Text)







class student_details(db.Model,UserMixin):
    
    Name=db.Column(db.Text)
    Rollno=db.Column(db.Integer,primary_key=True,)
    email=db.Column(db.Text)
    Class=db.Column(db.Text)
    Department=db.Column(db.Text)
    Sport=db.Column(db.Text)
    column_display_pk = True

    def __repr__(self):
        return '<student_details %r>' % (self.name)


class details(ModelView):
    form_columns = ['Name', 'Rollno', 'email', 'Class', 'Department','Sport',]

class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged in" in session:
            return True;
        else:
            abort(403);
        
   
    


class events(db.Model):

    column_display_pk = True
    Name=db.Column(db.Text)
    ID=db.Column(db.Integer,primary_key=True)
    Schedule=db.Column(db.Text)
    Rules=db.Column(db.Text)

    def __repr__(self):
        return '<events %r>' % (self.name)


class e(ModelView):
    form_columns = ['Name', 'ID',  'Schedule', 'Rules']



   




admin.add_view(details(student_details,db.session));
admin.add_view(ModelView(events,db.session));









@app.route("/",methods=["GET"])
def index():
    cursor=mydb.cursor();
    cursor.execute("SELECT * FROM events")

    myresult = cursor.fetchall()
    
    

    return render_template("/demo.html",data=myresult);

    




@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account :
            session['loggedin'] = True
            msg = 'Logged in successfully !'
            cursor=mydb.cursor();
            cursor.execute("SELECT * FROM events")  

            myresult = cursor.fetchall()
    
    

            return render_template("admin.html");
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html')



@app.route("/logout")
def  logout():
    session.clear()
    return redirect("/ ");
    
    

    
    

@app.route("/registrations", methods=(["GET","POST"]))
def insert():

    if request.method=="GET":
        return render_template("registrations.html")

    if request.method=="POST":
        name=request.form["name1"];
        number=request.form["number1"];
        class1=request.form["classes"];
        dep=request.form["department"];
        sport=request.form.getlist("sport");
        str1 = ','.join(sport);
        mail=request.form["email"];
        



        stud=student_details(Name=name,Rollno=number,email=mail,Class=class1,Department=dep,Sport=str1);
        db.session.add(stud);
        db.session.commit();


        return "success"    


@app.route("/form2")
def log2():
    return render_template("form2.html");




@app.route("/admin1",methods=(["GET","POST"]))
def addevent():
    if request.method=="GET":
        return render_template("form2.html")

    if request.method=="POST":
        name=request.form["name"];
        id=request.form["id"];
        sc=request.form["schedule"];
        rules=request.form["rules"];


    
        event=events(Name=name,ID=id,Schedule=sc,Rules=rules);
        db.session.add(event);
        db.session.commit();




        return redirect(url_for("index.html"));


@app.route("/index",methods=(["GET","POST"]))
def ind():
    
        if request.method=="GET":
            return render_template("index.html")

        if request.method=="POST":
            name=request.form["name"];
            id=request.form["id"];
            sc=request.form["schedule"];
            rules=request.form["rules"];
            event=events(Name=name,ID=id,Schedule=sc,Rules=rules);
            db.session.add(event);
            db.session.commit();
        
            cursor=mydb.cursor();
            cursor.execute("SELECT * FROM events")

            myresult = cursor.fetchall()
            
    
    

            return render_template("index.html",data=myresult);

    
    
        

@app.route("/addd")
def log21():
    todos=events.query.all();
    return render_template("Home.html",todos=todos)

       


    
    


       

app.run(debug=True)




    

   