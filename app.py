from datetime import datetime
import requests
from flask import Flask, render_template, request, redirect, session, make_response, send_file,jsonify
from mysql.connector import connect
from flask_mail import Mail, Message
import random
from random import randint
import string
app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='robins19.k@gmail.com',
    MAIL_PASSWORD='Robins@08'
)
app.secret_key='ghjhjhq/213763fbf'

mail=Mail(app)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/<url>')
def dynamicUrl(url):
    connection = connect(host="localhost", database="student", user="root", password="Robins",port='3305')
    cur = connection.cursor()
    query1 = "select * from urlinfo where encryptedUrl='{}'".format(url)
    cur.execute(query1)
    orignalurl = cur.fetchone()
    if orignalurl==None:
        return render_template('index.html')
    else:
        print(orignalurl[1])
        return redirect(orignalurl[1])


@app.route('/urlshortner')
def urlshortner():
    # letter='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    url = request.args.get('link')
    custom = request.args.get('customurl')
    print(custom)
    print("planettech")
    connection = connect(host="localhost", database="student", user="root", password="Robins",port='3305')
    cur = connection.cursor()
    encryptedurl=''
    if custom=='':
        while True:
            encryptedurl=createEncrytedUrl()
            query1="select * from urlinfo where encryptedUrl='{}'".format(encryptedurl)
            cur.execute(query1)
            xyz=cur.fetchone()
            if xyz==None:
                break
        print(encryptedurl)
        if 'userid' in session:
            id=session['userid']
            query = "insert into urlinfo(orignalUrl,encryptedUrl,is_Active,created_by) values('{}','{}',1,{})".format(url, encryptedurl,id)
        else:
            query = "insert into urlinfo(orignalUrl,encryptedUrl,is_Active) values('{}','{}',1)".format(url,encryptedurl)
        cur = connection.cursor()
        cur.execute(query)
        connection.commit()
        finalencryptedurl = 'sd.in/' + encryptedurl
    else:
        query1 = "select * from urlinfo where encryptedUrl='{}'".format(custom)
        cur.execute(query1)
        xyz = cur.fetchone()
        if xyz==None:
            if 'userid' in session:
                id = session['userid']
                query = "insert into urlinfo(orignalUrl,encryptedUrl,is_Active,created_by) values('{}','{}',1,{})".format(url,custom,id)
            else:
                query = "insert into urlinfo(orignalUrl,encryptedUrl,is_Active) values('{}','{}',1)".format(url, custom, 1)
            cur = connection.cursor()
            cur.execute(query)
            connection.commit()
            finalencryptedurl = 'sd.in/' +custom
        else:
            return "url already exist"
    if 'userid' in session:
        return redirect('/home')
    else:
        return render_template('index.html',finalencryptedurl=finalencryptedurl,url=url)

def createEncrytedUrl():
    letter = string.ascii_letters + string.digits
    encryptedurl = ''
    for i in range(6):
        encryptedurl = encryptedurl + ''.join(random.choice(letter))
    print(encryptedurl)
    return encryptedurl

@app.route('/signup')
def signup():
    return render_template('SignUp.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/checkLoginIn')
def checkLogIn():
    email=request.args.get('email')
    password=request.args.get('pwd')
    connection = connect(host="localhost", database="student", user="root", password="Robins",port='3305')
    cur = connection.cursor()
    query1 = "select * from userdetails where emailId='{}'".format(email)
    cur.execute(query1)
    xyz = cur.fetchone()
    print(xyz)
    if xyz == None:
        return render_template('Login.html', xyz='you are not registered')
    else:
        if password==xyz[3]:
            session['email']=email
            session['userid']=xyz[0]
            #return render_template('UserHome.html')
            return redirect('/home')
        else:
            return render_template('Login.html', xyz='your password is not correct')


@app.route('/register',methods=['post'])
def register():
    email=request.form.get('email')
    username=request.form.get('uname')
    password=request.form.get('pwd')
    connection = connect(host="localhost", database="student", user="root", password="Robins",port='3305')
    cur = connection.cursor()
    query1 = "select * from userdetails where emailId='{}'".format(email)
    cur.execute(query1)
    xyz = cur.fetchone()
    if xyz==None:
        #file=request.files['file']
        #print(type(file))
       # file.save('F:/files/'+file.filename)
        query = "insert into userdetails(emailId,userName,password,is_Active,created_Date) values('{}','{}','{}',1,now())".format(email, username, password)
        cur = connection.cursor()
        cur.execute(query)
        connection.commit()
        return 'you are successfully registered'

    else:
        return 'already registered'
#@app.route('/google')
#def google():
    #path='D:/Demo/as.jpg'
    #return send_file(path,mimetype='image/jpg',as_attachment=True)
    #(iske use se hum kahi se bhi kisi file ko iss directory se download karwa sakte hai)

@app.route('/google')
def google():
    return render_template('google.html')

@app.route('/home')
def home():
    if 'userid' in session:
        email=session['email']
        id=session['userid']
        print(id)
        connection = connect(host="localhost", database="student", user="root", password="Robins",port='3305')
        cur = connection.cursor()
        query1 = "select * from urlinfo where created_by={}".format(id)
        cur.execute(query1)
        data=cur.fetchall()
        print(data)
        return render_template('updateUrl.html',data=data)
    return render_template('login.html')
@app.route('/editUrl',methods=['post'])
def editUrl():
    if 'userid' in session:
        email = session['email']
        print(email)
        id=request.form.get('id')
        url=request.form.get('orignalurl')
        encrypted=request.form.get('encrypted')
        return render_template("editUrl.html",url=url,encrypted=encrypted,id=id)
    return render_template('login.html')

@app.route('/updateUrl',methods=['post'])
def updateUrl():
    if 'userid' in session:
        id=request.form.get('id')
        url=request.form.get('orignalurl')
        encrypted=request.form.get('encrypted')
        connection = connect(host="localhost", database="student", user="root", password="Robins",port='3305')
        cur = connection.cursor()
        query = "select * from urlinfo where encryptedurl='{}'and pk_urlId!={}".format(encrypted,id)
        cur.execute(query)
        data = cur.fetchone()
        if data==None:
            query1 = "update urlinfo set orignalUrl='{}', encryptedUrl='{}' where pk_urlId={}".format(url,encrypted,id)
            cur.execute(query1)
            connection.commit()
            return redirect('/home')
        else:
            return render_template("editUrl.html", url=url, encrypted=encrypted, id=id,error='short url already exist')
    return render_template("login.html")

@app.route('/deleteUrl',methods=['post'])
def deleteUrl():
    if 'userid' in session:
        id = request.form.get('id')
        connection = connect(host="localhost", database="student", user="root", password="Robins",port='3305')
        cur = connection.cursor()
        query1 = "delete from urlinfo where pk_urlId="+id
        cur.execute(query1)
        connection.commit()
        return redirect('/home')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('userid',None)
    return render_template('login.html')


@app.route('/askemail')
def askemail():
    return render_template('askemail.html')

@app.route('/forget')
def forgetpassword():
    email = request.args.get('email')
    randomnumber = ''
    letter = string.digits
    for i in range(6):
        randomnumber = randomnumber + ''.join(random.choice(letter))
    body = 'Your forget password OTP is ' + randomnumber
    msg = Message(subject='Forget Password Email ', sender='robins19.k@gmail.com',
                  recipients=[email], body=body)
    msg.cc = [email]
    mail.send(msg)
    connection = connect(host="localhost", database="student", user="root", password="Robins",port='3305')
    cur = connection.cursor()
    query2 = "select * from userdetails where emailId='{}'".format(email)
    cur.execute(query2)
    data = cur.fetchone()
    if data == None:
        return "You are not registered"
    query1 = "update userdetails set otp ='{}' where emailId= '{}'".format(randomnumber, email)
    cur.execute(query1)
    connection.commit()
    return render_template('updatepassword.html', email=email)

@app.route('/updatepassword')
def updatepassword():
    emailId = request.args.get('email')
    otp = request.args.get('otp')
    pwd = request.args.get('pwd')
    connection = connect(host="localhost", database="student", user="root", password="Robins", port='3305')
    cur = connection.cursor()
    query1 = "select * from userdetails where emailId='{}'".format(emailId)
    cur.execute(query1)
    data = cur.fetchone()
    print(data)
    if int(data[8])==int(otp):
        query2 = "update userdetails set password ='{}' where emailId= '{}'".format(pwd,emailId)
        cur.execute(query2)
        connection.commit()
        return "Your password has been successfully changed"
    else:
        return "Worng OTP"

@app.route('/apitest',methods=['post'])
def api():
    abc1=request.get_json()
    print(abc1)
    list=[]
    da={}
    connection = connect(host="localhost", database="student", user="root", password="Robins", port='3305')
    cur=connection.cursor()
    query="select * from urlinfo"
    cur.execute(query)
    data=cur.fetchall()
    for i in data:
        da["name"]=i[0]
        da["email"]=i[1]
        list.append(da)
    dict={'name':"Robins"}
    return jsonify(list)

@app.route('/apitest1',methods=['post'])
def api1():
    abc1=request.get_json()
    print(abc1)
    dict={'name':"Robins"}
    return jsonify(dict)



if __name__ == "__main__":
    app.run()