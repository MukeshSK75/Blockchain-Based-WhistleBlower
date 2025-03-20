from flask import Flask,redirect,url_for,render_template,request,session
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import os
import time
from datetime import datetime
import random
import string
import time
from flask_login import UserMixin
from bit import Key





app = Flask(__name__)
TEMPLATE_DIR = os.path.join('templates')
picf=os.path.join('static','pic')
SECRET_KEY = "THIS SECRET"
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://somas:XpJYUz9uAFxCQHKOr6OEwAc3h4OwlePi@dpg-curoe03v2p9s7390ft2g-a.oregon-postgres.render.com/log_3c6n'
app.config['TEMPLATE_FOLDER']=TEMPLATE_DIR
app.config['UPLOAD_FOLDER']=picf
db=SQLAlchemy(app)



class logger(db.Model,UserMixin):
    __tablename__='logs'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(25),unique=True,nullable=False)
    password=db.Column(db.String(),nullable=False)
    uid=db.Column(db.String(16),unique=True,nullable=False)
    emaill=db.Column(db.String(),unique=True,nullable=False)



class Post(db.Model,UserMixin):
    __tablename__='blogcontent'
    id = db.Column(db.Integer, primary_key=True)
    title =db.Column(db.String(50))
    date_created = db.Column(db.DateTime(timezone=True))
    author = db.Column(db.String(50))
    text = db.Column(db.Text, nullable=False)
   # author = db.Column(db.Integer, db.ForeignKey(
    #    'user.id', ondelete="CASCADE"), nullable=False)

def generate_custom_id():
    timestamp = str(int(time.time()))
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{timestamp}{random_chars}"
   
def valilog(us,ps):
    u_l=logger.query.filter_by(uid=us).first()
    if u_l is None:
        raise ValidationError("INCORRECT US OR PS")
    elif ps != u_l.password:
        raise ValidationError("INCORRECT US OR PS")

class pri:
    key = Key()
    private_key = key.to_wif()
    bitcoin_address = key.address


class NamerForm(FlaskForm):
    uuids=StringField("ID: ",validators=[DataRequired()])   
    passw=PasswordField("PASSWORD: ",validators=[DataRequired()])
    sub=SubmitField(label='Submit')

class regform(FlaskForm):
    namer=StringField("NAME: ",validators=[DataRequired()])
    emailr=EmailField("EMAIL: ",validators=[DataRequired()])   
    passwr=PasswordField("PASSWORD: ",validators=[DataRequired(),Length(min=4,max=20,message="password must be >4 and <20")])
    cpr=PasswordField("CONFRIM PASSWORD: ",validators=[DataRequired(),EqualTo(passwr,message="pass dont match")])
    subr=SubmitField("SUBMIT")

    def vali(self,userm,namr):
        uo=logger.query.filter_by(emaill=userm).first()
        noo=uo=logger.query.filter_by(username=namr).first()
        if uo or noo:
            raise ValidationError("USER NAME ALREADY EXIST")

class PostForm(FlaskForm):
    t=StringField(label='Name', validators=[DataRequired(),Length(max=20)]) 
    a=StringField(label='Author', validators=[DataRequired(),Length(max=25)])
    c=StringField(label='CONTENT', validators=[DataRequired()])
    submit = SubmitField(label="Post")


@app.route('/', methods=['GET','POST'])
def hom():
   
   pic1=os.path.join(app.config['UPLOAD_FOLDER'],'futuristic.webp')
   pic2=os.path.join(app.config['UPLOAD_FOLDER'],'ss.jpeg')
   return render_template('landi.html',userim=pic1,userim2=pic2)

@app.route('/login', methods=['GET','POST'])
def login():
   
   passw=None
   uuids=None
   form=NamerForm()
   csl=os.path.join(app.config['UPLOAD_FOLDER'],'style.css')
   if request.method == 'POST' and form.validate_on_submit:
       username=form.uuids.data
       password=form.passw.data
       valilog(username,password)
       session['user']=username
       return redirect(url_for('view'))
   else:
       if "user" in session:
           return redirect(url_for('view')) 
       return render_template('login.html', form=form,uuids=uuids,passw=passw,scc=csl)

@app.route('/register', methods=['GET','POST'])
def register():
   namer=None
   emailr=None
   passwr=None
   x=None
   cpr=None
   reg=regform()
   csl=os.path.join(app.config['UPLOAD_FOLDER'],'style.css')
   if request.method == 'POST' and reg.validate_on_submit:
       
       userna=reg.namer.data
       passwo=reg.passwr.data
       userem=reg.emailr.data
       x=generate_custom_id()
       reg.vali(userem,userna)
       user=logger(username=userna,password=passwo,uid=x,emaill=userem)
       db.session.add(user)
       db.session.commit()
       return redirect(url_for('login', next=request.endpoint))
   else:
       if "user" in session:
           return redirect(url_for('view')) 
   return render_template('register.html', reg=reg,namer=namer,emailr=emailr,passwr=passwr,x=x,cpr=cpr,scc=csl)
@app.route('/post',methods=['GET','POST'])
def post():
    t=None
    a=None
    c=None
    pf=PostForm()
    csl=os.path.join(app.config['UPLOAD_FOLDER'],'poststyles.css')
    if "user" in session:
        if request.method=='POST':
            tt=pf.t.data
            aa=pf.a.data
            cc=pf.c.data
            timestamp = time.time()  # Get the current timestamp
            date_time = datetime.fromtimestamp(timestamp)  # Convert timestamp to datetime object
            formatted_string = date_time.strftime("%Y-%m-%d %H:%M:%S")
            addr=Post(title=tt,author=aa,text=cc,date_created=formatted_string)
            db.session.add(addr)
            db.session.commit()
            return "ADDED" and redirect(url_for('view'))
    else:
       return redirect(url_for('login'))
    return render_template('posting.html',pf=pf,t=t,a=a,c=c,pss=csl)

@app.route('/view')
def view():
    
    if "user" in session:
        posts=Post.query.order_by(Post.date_created.desc()).all()
        return render_template('pp.html',posts=posts)
    else:
        return redirect(url_for('login'))

@app.route('/loc/<int:post_id>')
def loc(post_id):
    csl=os.path.join(app.config['UPLOAD_FOLDER'],'poststyle.css')
    if "user" in session:
        loc=Post.query.filter_by(id=post_id).one()
        return render_template('viewpost.html',loc=loc,scc=csl)
    else:
         return redirect(url_for('login'))

@app.route('/wallet')
def wallet():
    csl=os.path.join(app.config['UPLOAD_FOLDER'],'style.css')
    if "user" in session:
        return render_template('wallet.html',scc=csl)
    else:
        return redirect(url_for('login'))


@app.route('/Register_Wallet')
def Register_Wallet():
    csl=os.path.join(app.config['UPLOAD_FOLDER'],'style.css')
    ss=None
    if "user" in session:
        ss = logger.query.filter_by(uid=session['user']).one()
        kk=pri.bitcoin_address
        return render_template('Register_Wallet.html',ss=ss,kk=kk,scc=csl)
    else:
        return redirect(url_for('login'))
    
@app.route('/Getid')
def Getid():
    csl=os.path.join(app.config['UPLOAD_FOLDER'],'style.css')
    if "user" in session:
        return render_template('Getid.html',scc=csl)
    else:
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session.pop("user",None)
    return redirect(url_for('login'))
if __name__=='__main__':
    app.run(debug=True)

