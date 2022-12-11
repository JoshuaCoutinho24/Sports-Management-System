from flask import Flask,render_template,request,abort,redirect,url_for,jsonify,make_response
from flask_admin import Admin,AdminIndexView,BaseView,expose
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_login import UserMixin,LoginManager,current_user,login_user
from flask import session
import mysql.connector
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField




app = Flask(__name__)
admin=Admin(app)



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




class logout(BaseView):
    @expose("/")
    def logou(self):
        return redirect("/logout")

class Dashboard(BaseView):
    @expose("/")
    def log(self):
        return redirect("/dashboard")
        









class student_details(db.Model,UserMixin):
    
    Name=db.Column(db.Text)
    Rollno=db.Column(db.Integer,primary_key=True,)
    email=db.Column(db.Text)
    Class=db.Column(db.Text)
    Department=db.Column(db.Text)
    
    column_display_pk = True

    def __repr__(self):
        return '<student_details %r>' % (self.name)


class sdetails(ModelView):
    column_display_pk=True;
    form_columns = ['Name', 'Rollno', 'email', 'Class', 'Department']

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
    column_display_pk=True;
    form_columns = ['Name', 'ID',  'Schedule', 'Rules']



class sport(db.Model):
    S_rollno=db.Column(db.Integer,primary_key=True);
    Sport=db.Column(db.Text);

    def __repr__(self):
        return '<sport %r>' % (self.name)


class e2(ModelView):
    column_display_pk=True;
    form_columns = ['S_rollno', 'Sport']    



   




admin.add_view(sdetails(student_details,db.session));
admin.add_view(e(events,db.session));
admin.add_view(e2(sport,db.session));
admin.add_view(Dashboard( name="DashBoard" ));
admin.add_view(logout( name="Logout" ));










@app.route("/",methods=["GET"])
def index():
    cursor=mydb.cursor();
    cursor.execute("SELECT * FROM events")

    myresult = cursor.fetchall()
    
    

    return render_template("/Home.html",data=myresult);

    




@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        index()
        if account :
            session['loggedin'] = True
            msg = 'Logged in successfully !'
             

            c=mydb.cursor()
            c.execute("SELECT * FROM events")

            myresult = c.fetchall()
    
    
    
    

            return render_template("admin.html",x=myresult);
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
        sport1=request.form.getlist("sport");
        str1 = ','.join(sport1);
        mail=request.form["email"];
        



        stud=student_details(Name=name,Rollno=number,email=mail,Class=class1,Department=dep);
        db.session.add(stud);
        db.session.commit();
        sp=sport(  S_rollno=number,Sport=str1)
       
        db.session.add(sp);
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
        c=mydb.cursor()
        c.execute("SELECT * FROM events")

        myresult = c.fetchall()
    
    
    
    

        return render_template("admin.html",x=myresult);




        return redirect(url_for("index.html"));


@app.route("/index",methods=(["GET","POST"]))
def ind():
    
        
            
        
            cursor=mydb.cursor();
            cursor.execute("SELECT * FROM events")

            myresult = cursor.fetchall()
            
    
    

            return render_template("index.html",data=myresult);

    
    
        

@app.route("/reroute")
def log21(id):
    id=request.forms["id1"];
     
    cursor=mydb.cursor();
    query=("SELECT * FROM events where ID=%s")
    cursor.execute(query,id)

    myresult = cursor.fetchall()
    return render_template("index.html",data=myresult);

    


@app.route("/admin",methods=["GET","POST"])
def func():

    count = student_details.query.filter_by(Sport="Basketball").count();
    print(count);
    cursor=mydb.cursor();
    cursor.execute("SELECT * FROM events")

    myresult = cursor.fetchall()
    
    

    return redirect("/admin",myresult=count,my1=myresult)

    

@app.route("/dashboard")
def f():
    
    basketball = sport.query.filter_by(Sport="Basketball").count();
    football = sport.query.filter_by(Sport="Football").count();
    Volleyball = sport.query.filter_by(Sport="Volleyball").count();

    cursor=mydb.cursor();
    cursor.execute("SELECT * from basketball_registrations")
   

    bb = cursor.fetchall()
    cursor.execute("SELECT * from football_registrations")
    ff=cursor.fetchall();


    cursor.execute("SELECT  Name,Rollno,Sport FROM student_details LEFT JOIN sport ON student_details.Rollno = sport.S_rollno INTERSECT SELECT  Name,Rollno,Sport FROM student_details RIGHT JOIN sport ON student_details.Rollno = sport.S_rollno")
    intersect=cursor.fetchall();

    cursor.execute("SELECT * FROM `past_events`")
    tri=cursor.fetchall();

    
    
    

    return render_template("demo.html",football=football,basketball=basketball, Volleyball=Volleyball,bb=bb,ff=ff,intersect=intersect,tri=tri)





    



       


    
    


       

app.run(debug=True)

