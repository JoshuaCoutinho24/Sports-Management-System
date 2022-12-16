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

from functools import wraps


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

# login=LoginManager(app);


# @login.user_loader
# def userid(id):
#     return user.query.get(int(id))
    

def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

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


class Addevents(BaseView):
    @expose("/")
    def log(self):
        return redirect("/form2")


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
            abort(404);
        




class events(db.Model):

    column_display_pk = True
    Name=db.Column(db.Text)
    ID= db.Column(db.Integer,primary_key=True)
    Schedule=db.Column(db.Text)
    Rules=db.Column(db.Text)

    def __repr__(self):
        return '<events %r>' % (self.name)


class e(ModelView):
    column_display_pk=True;
    form_columns = ['Name', 'ID',  'Schedule', 'Rules']



class sport(db.Model):
    id=db.Column(db.Integer,primary_key=True);
    S_rollno=db.Column(db.Integer);
    Sport=db.Column(db.Text);

    def __repr__(self):
        return '<sport %r>' % (self.name)


class e2(ModelView):
    
    form_columns = ['S_rollno', 'Sport']



admin.add_view(sdetails(student_details, db.session, name="Student Details"));
admin.add_view(e(events, db.session, name="Events"));
admin.add_view(e2(sport, db.session, name="Sports"));
admin.add_view(Dashboard(name="DashBoard"));
admin.add_view(Addevents(name="Add Event"));
admin.add_view(logout(name="Logout"));






@app.route("/",methods=["GET"])
def index():
    cursor=mydb.cursor();
    cursor.execute("SELECT * FROM events")

    myresult = cursor.fetchall()
    

    return render_template("Home.html",data=myresult);




@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        select = request.form['log']
        dep = request.form['dep']
        
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account and select=="Coordinator" :
            session['user_id'] = account[0]
            msg = 'Logged in successfully!'
            return redirect("/admin");

        if account and select=="Faculty" and dep=='COMP':
            session['user_id'] = account[0]
            msg = 'Logged in successfully!'
            return redirect("/COMP");


        if account and select=="Faculty" and dep=='CIVIL':
            session['user_id'] = account[0]
            msg = 'Logged in successfully!'
            return redirect("/CIVIL");


        if account and select=="Faculty" and dep=='MECH':
            session['user_id'] = account[0]
            msg = 'Logged in successfully!'
            return redirect("/MECH");


        if account and select=="Faculty" and dep=='ETC':
            session['user_id'] = account[0]
            msg = 'Logged in successfully!'
            return redirect("/ETC");


        
    
            
        else:
            msg = 'Incorrect username/password!'
            return render_template('error.html',msg=msg)
    else:
        return render_template("login.html")


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
        mail=request.form["email"];


        stud=student_details(Name=name,Rollno=number,email=mail,Class=class1,Department=dep);
        db.session.add(stud);
        db.session.commit();

        for str1 in sport1:
            sp=sport(S_rollno=number,Sport=str1);
            db.session.add(sp);
            db.session.commit();
        


        return redirect("/");    


@app.route("/form2")
@login_required
def log2():
    return render_template("form2.html");




@app.route("/admin1",methods=(["GET","POST"]))
@login_required
def addevent():
    if request.method=="GET":
        return render_template("form2.html")

    if request.method=="POST":
        name=request.form["name"];
        id=request.form["id"];
        sc=request.form["schedule"];
        rules=request.form["rules"];


        
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO events (Name,ID,Schedule,rules) VALUES(%s,%s,%s,%s)''',(name,id,sc,rules))
        mysql.connection.commit()
        cursor.close()
        # event=events(Name=name,ID=id,Schedule=sc,Rules=rules);
        # db.session.add(event);
        # db.session.commit();
        # c=mydb.cursor()
        # c.execute("SELECT * FROM events")
        # myresult = c.fetchall()
    
    
    
    

        return redirect("/")




        #return redirect(url_for("index.html"));


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
@login_required
def func():
    cursor=mydb.cursor();
    cursor.execute("SELECT * FROM events")

    myresult = cursor.fetchall()


    return render_template("Home.html",data=myresult)



@app.route("/dashboard")
@login_required
def f():

    basketball = sport.query.filter_by(Sport="Basketball").count();
    football = sport.query.filter_by(Sport="Football").count();
    Volleyball = sport.query.filter_by(Sport="Volleyball").count();

    cursor=mydb.cursor();

    cursor.execute("SELECT * from basketball_registrations ORDER BY S_rollno;")
    bb = cursor.fetchall()
    
    cursor.execute("SELECT * from football_registrations ORDER BY S_rollno;")
    ff=cursor.fetchall();

    cursor.execute("SELECT * from volleyball_registrations ORDER BY S_rollno;")
    vv=cursor.fetchall();

    cursor.execute("SELECT Name, Rollno, Sport FROM student_details LEFT JOIN sport ON student_details.Rollno = sport.S_rollno ORDER BY S_rollno;;")
    intersect=cursor.fetchall();

    cursor.execute("SELECT Name, Department FROM student_details UNION ALL SELECT Name, Department FROM faculty ORDER BY Department;")
    trial=cursor.fetchall();

    cursor.execute("SELECT * FROM `past_events`")
    tri=cursor.fetchall();

    

    return render_template("demo.html", football=football, basketball=basketball, Volleyball=Volleyball, bb=bb, ff=ff, vv=vv, intersect=intersect, tri=tri, trial=trial)


@app.route("/COMP")
@login_required
def coord1():
    cursor=mydb.cursor();
    
    cursor.execute("SELECT `Name`,`Rollno`,`Class`,`Department` FROM `student_details` WHERE Department='Computer'");
    basketball = cursor.fetchall();
    
    cursor.execute("SELECT `Name`,`Rollno`,`Class`,`Department`,`Sport` FROM `student_details` as t1 INNER JOIN sport as t2 on t1.Rollno=t2.S_rollno WHERE Department='Computer' HAVING `Class`='SE'");
    football = cursor.fetchall()
    
    cursor.execute("SELECT `Name`,`Rollno`,`Class`,`Department`,`Sport` FROM `student_details` as t1 INNER JOIN sport as t2 on t1.Rollno=t2.S_rollno WHERE Department='Computer' HAVING `Class`='TE'")
    Volleyball = cursor.fetchall()


    cursor.execute("SELECT `Name`,`Rollno`,`Class`,`Department`,`Sport` FROM `student_details` as t1 INNER JOIN sport as t2 on t1.Rollno=t2.S_rollno WHERE Department='Computer' HAVING `Class`='BE'")
    Volleyball1 = cursor.fetchall()



    return render_template("x.html",  basketball=basketball,football=football,Volleyball=Volleyball,Volleyball1=Volleyball1 )



@app.route("/CIVIL")
@login_required
def coord2():
    cursor=mydb.cursor();
    
    cursor.execute("SELECT `Name`,`Rollno`,`Class`,`Department` FROM `student_details` WHERE Department='Civil'");
    basketball = cursor.fetchall();
    
    cursor.execute("SELECT `Name`,`Rollno`,`Class`,`Department`,`Sport` FROM `student_details` as t1 INNER JOIN sport as t2 on t1.Rollno=t2.S_rollno WHERE Department='Civil' HAVING `Class`='SE'");
    football = cursor.fetchall()
    
    cursor.execute("SELECT `Name`,`Rollno`,`Class`,`Department`,`Sport` FROM `student_details` as t1 INNER JOIN sport as t2 on t1.Rollno=t2.S_rollno WHERE Department='Civil' HAVING `Class`='TE'")
    Volleyball = cursor.fetchall()


    cursor.execute("SELECT `Name`,`Rollno`,`Class`,`Department`,`Sport` FROM `student_details` as t1 INNER JOIN sport as t2 on t1.Rollno=t2.S_rollno WHERE Department='Civil' HAVING `Class`='BE'")
    Volleyball1 = cursor.fetchall()



    return render_template("x.html",  basketball=basketball,football=football,Volleyball=Volleyball,Volleyball1=Volleyball1 )



@app.route("/MECH")
@login_required
def coord3():
    cursor=mydb.cursor();
    
    cursor.execute("SELECT `Name`,`Rollno`,`Class`,`Department` FROM `student_details` WHERE Department='Mechanical'");
    basketball = cursor.fetchall();
    
    cursor.execute("SELECT `Name`,`Rollno`,`Class`,`Department`,`Sport` FROM `student_details` as t1 INNER JOIN sport as t2 on t1.Rollno=t2.S_rollno WHERE Department='Mechanical' HAVING `Class`='SE'");
    football = cursor.fetchall()
    
    cursor.execute("SELECT `Name`,`Rollno`,`Class`,`Department`,`Sport` FROM `student_details` as t1 INNER JOIN sport as t2 on t1.Rollno=t2.S_rollno WHERE Department='Mechanical' HAVING `Class`='TE'")
    Volleyball = cursor.fetchall()


    cursor.execute("SELECT `Name`,`Rollno`,`Class`,`Department`,`Sport` FROM `student_details` as t1 INNER JOIN sport as t2 on t1.Rollno=t2.S_rollno WHERE Department='Mechanical' HAVING `Class`='BE'")
    Volleyball1 = cursor.fetchall()



    return render_template("x.html",  basketball=basketball,football=football,Volleyball=Volleyball,Volleyball1=Volleyball1 )



@app.route("/ETC")
@login_required
def coord4():
    cursor=mydb.cursor();
    
    cursor.execute("SELECT `Name`,`Rollno`,`Class`,`Department` FROM `student_details` WHERE Department='ETC'");
    basketball = cursor.fetchall();
    
    cursor.execute("SELECT `Name`,`Rollno`,`Class`,`Department`,`Sport` FROM `student_details` as t1 INNER JOIN sport as t2 on t1.Rollno=t2.S_rollno WHERE Department='ETC' HAVING `Class`='SE'");
    football = cursor.fetchall()
    
    cursor.execute("SELECT `Name`,`Rollno`,`Class`,`Department`,`Sport` FROM `student_details` as t1 INNER JOIN sport as t2 on t1.Rollno=t2.S_rollno WHERE Department='ETC' HAVING `Class`='TE'")
    Volleyball = cursor.fetchall()


    cursor.execute("SELECT `Name`,`Rollno`,`Class`,`Department`,`Sport` FROM `student_details` as t1 INNER JOIN sport as t2 on t1.Rollno=t2.S_rollno WHERE Department='ETC' HAVING `Class`='BE'")
    Volleyball1 = cursor.fetchall()



    return render_template("x.html",  basketball=basketball,football=football,Volleyball=Volleyball,Volleyball1=Volleyball1 )





@app.route("/dash")
def change():
    return render_template("dash.html");
app.run(debug=True)