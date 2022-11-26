from flask import Flask,render_template,request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL

app = Flask(__name__)
admin=Admin(app)


app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/test"
app.config['SECRET_KEY'] = 'mysecret'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test'


db= SQLAlchemy(app);  
mysql=MySQL(app);


#Classes
class student_details(db.Model):
    Name=db.Column(db.Text)
    Rollno=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.Text)
    Class=db.Column(db.Text)
    Department=db.Column(db.Text)
    Sport=db.Column(db.Text)


   

admin.add_view(ModelView(student_details, db.session))







@app.route("/")
def index():
    return render_template("Home.html");


    

    
    

@app.route("/registrations", methods=(["GET","POST"]))
def insert():

    if request.method=="GET":
        return render_template("registrations.html")

    if request.method=="POST":
        name=request.form["name1"];
        number=request.form["number1"];
        class1=request.form["class"];
        dep=request.form["department"];
        sport=request.form["sport"];
        str1 = ','.join(sport);
        mail=request.form["email"];
        



        stud=student_details(Name=name,Rollno=number,email=mail,Class=class1,Department=dep,Sport=str1);
        db.session.add(stud);
        db.session.commit();

        return "Success";



app.run(debug=True)




    

   