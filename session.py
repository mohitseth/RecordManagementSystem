from flask import Flask, session, render_template, request,flash , redirect, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS,cross_origin
from datetime import datetime
import json
# from flask_mysqldb import MySQL
import os
from flask import jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/satyugdb'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
db = SQLAlchemy(app)
app.secret_key = os.urandom(24)


class Contact(db.Model):
    '''
    sno, name email subject message date
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(12), nullable=True)


class Books(db.Model):
	bsno = db.Column(db.Integer, primary_key=True)
	bseries = db.Column(db.String(10), nullable=False)
	dcode = db.Column(db.String(10), nullable=False)
	scode = db.Column(db.String(10), nullable=False)
	name = db.Column(db.String(20), nullable=False)
	date = db.Column(db.String(12), nullable=False)
	branch = db.Column(db.String(20), nullable=False)

class Branch(db.Model):
	bno = db.Column(db.Integer, primary_key=True)
	bname = db.Column(db.String(15), nullable=False)
	badmin = db.Column(db.String(15), nullable=False)
	baddress = db.Column(db.String(20), nullable=False)

class Dataentry(db.Model):
    '''
    sno, name email subject message date
    '''
    sid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(80), nullable=False)
    middle_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(40), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    bookseries = db.Column(db.String(10), nullable=False)
    branch = db.Column(db.String(15), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    pan = db.Column(db.String(20), nullable=False)
    rno = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    



@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)
        session['user'] = request.form['username']

        if request.form['password'] == 'password1' and session['user'] == 'mohitsethi':
            return redirect(url_for('index'))
        
        elif request.form['password'] == 'password2' and session['user'] == 'shaleentaneja':
            return redirect(url_for('index'))

        else:
            flash("Wrong username or password")
       

    return render_template('login.html')


@app.route('/index')
@cross_origin(supports_credentials=True)
def index():
    if g.user:
        return render_template('index.html')

    return redirect(url_for('login'))

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']

    return 'Not logged in!'

@app.route('/dropsession')
def dropsession():
    session.pop('user', None)
    return 'Dropped!'


@app.route('/about')
def about():
    if g.user:
        return render_template('about.html')

    return redirect(url_for('login'))


@app.route('/displayEntries')
def displayEntries():
    if g.user:
        entrydata = Dataentry.query.all()
        return render_template('display_entries.html',entrydata= entrydata)
        
    return redirect(url_for('login'))


@app.route('/addBook')
def addBook():
    if g.user:
    	branchdata = Branch.query.all()
    	return render_template('add_book.html' , branchdata=branchdata)
    	
    return redirect(url_for('login'))

@app.route('/viewBook')
def viewBook():
    if g.user:
    	bookdata = Books.query.all()
    	return render_template('view_books.html',bookdata= bookdata)

    return redirect(url_for('login'))


@app.route('/addEntry')
def addEntry():
    if g.user:
        branchdata = Branch.query.all()
        bookdata = Books.query.all()
        return render_template('add_entry.html' , branchdata=branchdata , bookdata=bookdata)

    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    # return render_template('login.html')
    return redirect(url_for('login'))



@app.route("/addBook", methods = ['GET', 'POST'])
def books():
    if(request.method=='POST'):
        
        bseries = request.form.get('bseries')
        dcode = request.form.get('dcode')
        scode = request.form.get('scode')
        name = request.form.get('name')
        date = request.form.get('date')
        branch = request.form.get('branch')
        entry = Books(bseries=bseries, dcode= dcode, scode= scode, name= name, date=date, branch=branch)
        db.session.add(entry)
        db.session.commit()
        flash('Data Successfully Inserted')
        
    return redirect(url_for('addBook',success=True))

@app.route("/addEntry", methods=['GET', 'POST'])
def dataentry():
    if (request.method == 'POST'):
        '''Add entry to the database'''
        flash("Data Inserted Successfully")
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        bookseries = request.form.get('bookseries')
        branch = request.form.get('branch')
        date = request.form.get('date')
        pan = request.form.get('pan')
        rno = request.form.get('rno')
        amount = request.form.get('amount')
        entry = Dataentry(first_name=first_name, middle_name=middle_name, last_name=last_name,address=address, city=city, state=state, bookseries=bookseries ,branch=branch , date=date , pan=pan , rno=rno,amount= amount)
        db.session.add(entry)
        db.session.commit()

    return redirect(url_for('addEntry', success=True))
    

@app.route('/deletebook/<int:id_data>', methods = ['GET'])
def deletebook(id_data):
    flash("Record Has Been Deleted Successfully")
    book = Books.query.get(id_data)
    db.session.delete(book)
    db.session.commit()

    return redirect(url_for('viewBook', success=True))

@app.route('/deleteentry/<int:id_data>', methods = ['GET'])
def deleteentry(id_data):
    flash("Record Has Been Deleted Successfully")
    entry = Dataentry.query.get(id_data)
    db.session.delete(entry)
    db.session.commit()

    return redirect(url_for('displayEntries', success=True))


# @app.route("/contact", methods = ['GET', 'POST'])
# def contact():
#     if(request.method=='POST'):
#         '''Add entry to the database'''
#         '''
#             sno, name email subject message date
#         '''
#         name = request.form.get('name')
#         email = request.form.get('email')
#         subject = request.form.get('subject')
#         message = request.form.get('message')
#         entry = Contact(name=name, email= email, subject= subject, date= datetime.now(), message=message)
#         db.session.add(entry)
#         db.session.commit()
        
#     return render_template(flash('form successully submitted'))


# @app.route("/add_entry", methods=['GET', 'POST'])
# def dataentry():
#     if (request.method == 'POST'):
#         '''Add entry to the database'''
#         flash("Data Inserted Successfully")
#         first_name = request.form.get('first_name')
#         middle_name = request.form.get('middle_name')
#         last_name = request.form.get('last_name')
#         address = request.form.get('address')
#         city = request.form.get('city')
#         state = request.form.get('state')
#         pin = request.form.get('pin')
#         phone = request.form.get('phone')
#         pan = request.form.get('pan')
#         sCode = request.form.get('sCode')
#         amount = request.form.get('amount')
#         entry = Dataentry(first_name=first_name, middle_name=middle_name, date=datetime.now(), last_name=last_name,
#                           address=address, city=city, state=state, pin=pin , pan=pan , phone=phone, sCode=sCode,amount= amount)
#         db.session.add(entry)
#         db.session.commit()

#     return redirect(url_for('protected', _anchor='portfolio', success=True))
#     # return render_template(flash('form successully submitted'))


# @app.route('/delete/<string:id_data>', methods = ['GET'])
# def delete(id_data):
#     flash("Record Has Been Deleted Successfully")
#     # cur = mysql.connection.cursor()
#     # cur.execute("DELETE FROM contact WHERE id=%s", (id_data,))
#     # mysql.connection.commit()
#     user = Dataentry.query.get(id_data)
#     db.session.delete(user)
#     db.session.commit()

#     return redirect(url_for('protected', _anchor='about', success=True))




# @app.route('/update',methods=['POST','GET'])
# def update():

#     if request.method == 'POST':
#         sid = request.form['sid']
#         first_name = request.form['first_name']
#         # middle_name = request.form['middle_name']
#         # last_name = request.form['last_name']
#         address = request.form['address']
#         # city = request.form['city']
#         # state = request.form['state']
#         # pin = request.form['pin']
#         phone = request.form['phone']
#         # pan = request.form['pan']
#         # sCode = request.form['sCode']
#         # amount = request.form['amount']

#         user = Dataentry.query.filter_by(sid)

#         user.first_name = first_name
#         # user.middle_name = middle_name
#         # user.last_name = last_name
#         user.address = address
#         # user.city = city
#         # user.state = state
#         # user.pin = pin
#         user.phone = phone
#         # user.pan = pan
#         # user.sCode = sCode
#         # user.amount = amount

#         session.commit()

#         # cur = mysql.connection.cursor()
#         # cur.execute("""
#         #        UPDATE contact
#         #        SET name=%s, email=%s, phone=%s
#         #        WHERE id=%s
#         #     """, (name, email, phone, id_data))
#         # mysql.connection.commit()
#         flash("Data Updated Successfully")
#         return redirect(url_for('protected', _anchor='about', success=True))




# @app.route('/preview')
# def display():
#     # cur = mysql.connection.cursor()
#     # cur.execute("SELECT  * FROM dataentry")
#     # data = cur.fetchall()
#     # cur.clos

#     mydata = Dataentry.query.all()
#     my_data_json = []
#     for i in mydata:
#         data = {}
#         data['first_name'] = i.first_name
#         data['sid'] = i.sid
#         data['last_name'] = i.last_name
#         data['middle_name'] = i.middle_name
#         data['address'] = i.address
#         # data['sid'] = i.sid
#         # data['sid'] = i.sid
#         # data['sid'] = i.sid
#         # data['sid'] = i.sid
#         # data['sid'] = i.sid
#         # data['sid'] = i.sid

#         my_data_json.append(data)
#     return jsonify(my_data_json)
if __name__ == '__main__':
    app.run(debug=True)