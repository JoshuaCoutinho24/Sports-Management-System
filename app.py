from flask import Flask,render_template,request,abort,redirect
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_login import UserMixin,LoginManager,current_user,login_user
from flask import session

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

login=LoginManager(app);


@login.user_loader
def userid(id):
    return student_details.query.get(id)
    


#Classes
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



   



admin.add_view(SecureModelView(student_details,db.session));
admin.add_view(e(events,db.session));








@app.route("/")
def index():
    return render_template("Home.html");



@app.route("/Home")
def index1():
    return render_template("Home.html");



@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        if request.form.get("name")=="Root" and request.form.get("password")=="Admin":
            session["logged in"]=True
            return redirect("/loggedin")   
    else:
        return render_template("login.html",failed=True)
    return render_template("login.html");
    



@app.route("/logout")
def  logout():
    session.clear()
    return redirect("/");
    
    

    
    

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


@app.route("/loggedin")
def log():
    return render_template("admin.html");




@app.route("/form2")
def log2():
    return render_template("form2.html");




@app.route("/addmain")
def addevent():
    if request.method=="GET":
        return render_template("form2.html")

    if request.method=="POST":
        name=request.form["name"];
        id=request.form["id"];
        sc=request.form["schedule"];
        rules=request.form["Rules"];


        event=student_details(Name=name,ID=id,Schedule=sc,Rules=rules);
        db.session.add(event);
        db.session.commit();


        return "Success";
        

        


    
    


       

app.run(debug=True)




    

   