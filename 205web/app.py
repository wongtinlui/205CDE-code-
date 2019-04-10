
import os
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
from flask_mysqldb import MySQL,MySQLdb
from flask_uploads import UploadSet, configure_uploads, IMAGES
from wtforms import Form, StringField, IntegerField, FloatField, TextAreaField, PasswordField, validators, SelectField
from wtforms.fields.html5 import EmailField
import datetime

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'nba'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/image/product'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


class LoginForm(Form):  # Create Login Form
    username = StringField('', [validators.length(min=1)],
                           render_kw={'autofocus': True, 'placeholder': 'Username'})
    password = PasswordField('', [validators.length(min=3)],
                             render_kw={'placeholder': 'Password'})

class LoginForm2(Form):  # Create Login Form
    username = StringField('', [validators.length(min=1)],
                           render_kw={'autofocus': True, 'placeholder': 'Username'})
    password = PasswordField('', [validators.length(min=3)],
                             render_kw={'placeholder': 'Password'})

class RegisterForm(Form):
    email = EmailField('', [validators.DataRequired(), validators.Email(), validators.length(min=4, max=25)],
                       render_kw={'placeholder': 'Email'})
    username = StringField('', [validators.length(min=3, max=25)], render_kw={'placeholder': 'Username'})
    
    password = PasswordField('', [validators.length(min=3)],
                             render_kw={'placeholder': 'Password'})
    address = StringField('', [validators.length(min=3, max=60)], render_kw={'placeholder': 'Address'})

class UpdateRegisterForm(Form):
    email = EmailField('', [validators.DataRequired(), validators.Email(), validators.length(min=4, max=25)],
                       render_kw={'placeholder': 'Email'})
    name = StringField('', [validators.length(min=3, max=25)], render_kw={'placeholder': 'Username'})
    
    pw = PasswordField('', [validators.length(min=3)],
                             render_kw={'placeholder': 'Password'})
    address = StringField('', [validators.length(min=3, max=60)], render_kw={'placeholder': 'Address'})

class UpdateProductForm(Form):
    name = StringField('', [validators.length(min=3, max=100)],
                            render_kw={'placeholder': 'Product Name'})
    detail = StringField('', [validators.length(min=3, max=500)],
                            render_kw={'placeholder': 'Detail'})
    price = FloatField('', [validators.InputRequired()], 
                            render_kw={'placeholder': 'Price'})
    ptype = StringField('', [validators.length(min=3, max=100)], 
                            render_kw={'placeholder': 'Product type'})
    plink = StringField('', [validators.length(min=3, max=100)], 
                            render_kw={'placeholder': 'Product Link'})

class OrderForm(Form):  # Create Order Form
    name = StringField('', [validators.length(min=1), validators.DataRequired()],
                       render_kw={'autofocus': True, 'placeholder': 'Full Name'})
    mobile_num = IntegerField('', [validators.InputRequired()],
                             render_kw={'autofocus': True, 'placeholder': 'Mobile'})
    quantity = SelectField('', [validators.DataRequired()],
                           choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    order_place = StringField('', [validators.length(min=1), validators.DataRequired()],
                              render_kw={'placeholder': 'Order Place'})

class UploadProductForm(Form):
    name = StringField('', [validators.length(min=3, max=100)],
                            render_kw={'placeholder': 'Product Name'})
    detail = StringField('', [validators.length(min=3, max=500)],
                            render_kw={'placeholder': 'Detail'})
    price = FloatField('', [validators.InputRequired()], 
                            render_kw={'placeholder': 'Price'})
    ptype = StringField('', [validators.length(min=3, max=100)], 
                            render_kw={'placeholder': 'Product type'})
                              
@app.route("/")
def index():
    return render_template ('index.html')

@app.route('/search', methods=['POST', 'GET'])
def search():
    form = OrderForm(request.form)
    print('in search')
    if 'search' in request.args:
        print('in 2')
        find = request.args['search']

        cur = mysql.connection.cursor()

        query_string = "SELECT * FROM products WHERE pname LIKE %s ORDER BY pid ASC"
        cur.execute(query_string, ('%' + find + '%',))
        products = cur.fetchall()

        cur.close()
        flash('Showing result for: ' + find, 'success')
        return render_template('search.html', products=products, form=form)
    else:
        flash('Search again', 'danger')
        return render_template('search.html')

@app.route("/store" , methods=['GET', 'POST'])
def store():
    cur = mysql.connection.cursor()
    values = 'tshirt'
    cur.execute("SELECT * FROM products WHERE ptype=%s ORDER BY RAND() ", (values,))
    tshirt = cur.fetchall()

    curq = mysql.connection.cursor()
    values = 'shorts'
    curq.execute("SELECT * FROM products WHERE ptype=%s ORDER BY RAND() ", (values,))
    shorts = curq.fetchall()
    return render_template ('store.html', tshirt=tshirt, shorts=shorts)

@app.route("/detail", methods=['GET', 'POST'])
def detail():
    form = OrderForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args['ordernow']
        now = datetime.datetime.now()
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        # Create Cursor
        curs = mysql.connection.cursor()
        uid = session['uid']
        curs.execute("INSERT INTO orders(uid, pid, name, mobile, place, quantity, date) "
                        "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                        (uid, pid, name, mobile, order_place, quantity, now_time))
        # Commit cursor
        mysql.connection.commit()

        # Close Connection
        curs.close()

        flash('Order successful', 'success')
        return redirect('store')
    if 'pid' in request.args:
        product_id = request.args['pid']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE pid=%s", (product_id,))
        product = curso.fetchall()
        return render_template('detail.html', product=product)
    elif 'order' in request.args:
        try:
            user = session['uid']

            product_id = request.args['order']
            curso = mysql.connection.cursor()
            curso.execute("SELECT * FROM products WHERE pid=%s", (product_id,))
            product = curso.fetchall()
            return render_template('order.html', product=product, form=form)
        except Exception:
            flash('Please Login', 'danger')
            return redirect('login')
    return render_template('detail.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # GEt user form
        username = form.username.data
        # password_candidate = request.form['password']
        password_candidate = form.password.data

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username=%s", [username])

        if result > 0:
            # Get stored value
            data = cur.fetchone()
            password = data['userpw']
            uid = data['userid']
            name = data['username']

            # Compare password
            if password_candidate == password:
                session['uid'] = uid
                session['uname'] = name

                print('user :',session['uname'],' sucess login')
                flash('Login Success', 'success')

                return redirect(url_for('index'))

            else:
                flash('Incorrect password', 'danger')
                return render_template('login.html', form=form)

        else:
            flash('Username not found', 'danger')
            # Close connection
            cur.close()
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        address = form.address.data

        # Create Cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users( useremail, username, userpw, useraddress) VALUES( %s, %s, %s, %s)",
                    (email, username, password, address))

        # Commit cursor
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash('You are now registered and can login', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', form=form)

@app.route("/logout")
def logout():
    session.clear()
    flash('Log out Success', 'success')
    return render_template ('index.html')

@app.route("/personal" , methods=['GET', 'POST'])
def personal():
    form = UpdateRegisterForm(request.form)
    try:
        userid = session['uid']
    except Exception:
        flash('Unauthorised! Please login', 'danger')
        return redirect(url_for('login'))

    curso = mysql.connection.cursor()
    curso.execute("SELECT * FROM users WHERE userid=%s", (userid,))
    result = curso.fetchone()

    if request.method == 'POST' and form.validate():
        useremail = form.email.data
        username = form.name.data
        userpw = form.pw.data
        useraddress = form.address.data

        # Create Cursor
        cur = mysql.connection.cursor()
        exe = cur.execute("UPDATE users SET useremail=%s, username=%s, userpw=%s, useraddress=%s WHERE userid=%s",
                        (useremail, username, userpw, useraddress, userid))
        mysql.connection.commit()

        if exe:
            flash('Profile updated', 'success')
            return render_template('personal.html', result=result, form=form)
        else:
            flash('Profile not updated', 'danger')
            return render_template('personal.html', result=result, form=form)

    return render_template('personal.html', result=result, form=form)

@app.route("/adminlogin" , methods=['GET', 'POST'])
def adminlogin():
    form = LoginForm2(request.form)
    if request.method == 'POST' and form.validate():
        # GEt user form
        username = form.username.data
        # password_candidate = request.form['password']
        password_candidate = form.password.data

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM admin WHERE adname=%s", [username])

        if result > 0:
            # Get stored value
            data = cur.fetchone()
            password = data['adpw']
            uid = data['adid']
            name = data['adname']

            # Compare password
            if password_candidate == password:
                session['adid'] = uid
                session['adname'] = name

                print('Admin :',session['adname'],' sucess login')

                return redirect(url_for('admin'))

            else:
                flash('Incorrect password', 'danger')
                return render_template('adminlogin.html', form=form)

        else:
            flash('Username not found', 'danger')
            # Close connection
            cur.close()
            return render_template('adminlogin.html', form=form)
    return render_template('adminlogin.html', form=form)

@app.route("/admin")
def admin():

    return render_template ('admin.html')

@app.route("/adalluser" , methods=['GET', 'POST'])
def adalluser():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users ")
    alluser = cur.fetchall()
    return render_template ('adalluser.html' ,alluser=alluser)

@app.route("/adallorders" , methods=['GET', 'POST'])
def adallorders():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM orders ")
    adallorders = cur.fetchall()
    return render_template ('adallorders.html' ,adallorders=adallorders)

@app.route("/delorder" , methods=['GET', 'POST'])
def delorder():
    if 'oid' in request.args:
        orderid = request.args['oid']
        curso = mysql.connection.cursor()
        curso.execute("DELETE FROM orders where oid=%s", (orderid,))
        mysql.connection.commit()
        try:
            session['adid']
            return redirect('adallorders')
        except Exception:
            return redirect('vieworders')
    return render_template ('delorder.html')

@app.route("/vieworders" , methods=['GET', 'POST'])
def vieworders():
    try:
        userid = session['uid']
    except Exception:
        flash('Please Login','danger')
        return render_template('login.html')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM orders WHERE uid=%s", (userid,))
    vieworders = cur.fetchall()
    return render_template ('vieworders.html' ,adallorders=vieworders)

@app.route("/adallpro", methods=['GET', 'POST'])
def adallpro():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products ")
    adallpro = cur.fetchall()
    return render_template ('adallpro.html' ,adallpro=adallpro)

@app.route("/delpro" , methods=['GET', 'POST'])
def delpro():
    if 'pid' in request.args:
        pid = request.args['pid']
        curso = mysql.connection.cursor()
        curso.execute("DELETE FROM products where pid=%s", (pid,))
        mysql.connection.commit()
    return redirect('adallpro')

@app.route("/editpro" , methods=['GET', 'POST'])
def editpro():
    if 'pid' in request.args:
        form = UpdateProductForm(request.form)
        pid = request.args['pid']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE pid=%s",(pid,))
        result = curso.fetchone()

        if request.method == 'POST' and form.validate():
            name = form.name.data
            detail = form.detail.data
            price = form.price.data
            ptype = form.ptype.data
            plink = form.plink.data

            # Create Cursor
            cur = mysql.connection.cursor()
            exe = cur.execute("UPDATE products SET pname=%s, pdetail=%s, pprice=%s, ptype=%s , plink=%s WHERE pid=%s",
                            ( name, detail, price, ptype, plink, pid))
            mysql.connection.commit()

            if exe:
                flash('info updated', 'success')
                return render_template('editpro.html', result=result, form=form)
            else:
                flash('info not updated', 'danger')
                return render_template('editpro.html', result=result, form=form)

        return render_template('editpro.html', result=result, form=form)
    return redirect('admin')

@app.route("/upload" , methods=['GET', 'POST'])
def upload():
    form = UploadProductForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        detail = form.detail.data
        price = form.price.data
        ptype = form.ptype.data

        file = request.files['picture']
        if name and detail and price and ptype and file:
            pic = file.filename
            photo = pic.replace("'", "")
            picture = photo.replace(" ", "_")
            if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
                savepic = photos.save(file, folder=ptype)
                if savepic:
                    curs = mysql.connection.cursor()
                    curs.execute("INSERT INTO products( pname, pdetail, pprice, ptype, plink)"
                                    "VALUES(%s, %s, %s, %s, %s)",
                                    (name, detail, price, ptype, picture))
                    mysql.connection.commit()
                    flash('Product added successful', 'success')
                    return render_template ('upload.html', form=form)
                else:
                    flash('Picture not save', 'danger')
                    return render_template ('upload.html', form=form)
            else:
                flash('File not supported', 'danger')
                return render_template ('upload.html', form=form)
        else:
            flash('Missing Information', 'danger')
            return render_template ('upload.html', form=form)
    return render_template ('upload.html', form=form)

@app.route("/about")
def about():
    return render_template ('about.html')

if __name__ == "__main__":
    app.secret_key = 'qwertyasdfg'
    app.run(debug=True)
