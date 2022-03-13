from flask import Flask,render_template,request,redirect,session
import pymysql

app = Flask(__name__)
app.secret_key = "ssfksfj898d"#just a random string of characters.


@app.route('/',methods=['POST','GET'])
def index():
    return render_template('index.html')

@app.route('/about',methods=['POST','GET'])
def about():
    return render_template('about.html')

@app.route('/products',methods=['POST','GET'])
def products():
    conn = makeConnection()
    cur = conn.cursor()
    sql = "SELECT * FROM products ORDER BY product_id ASC"
    cur.execute(sql)
    if(cur.rowcount >= 1):
        return render_template("products.html",result = cur.fetchall())
    else:
        return render_template('products.html',result = "No Products Found")

@app.route('/contacts',methods=['POST','GET'])
def contacts():
    return render_template('contacts.html')

@app.route('/home',methods=['POST','GET'])
def home():
    if 'username' in session:
        return render_template('home.html')
    else:
        return render_template('login.html',msg="Please Login First")


@app.route('/add-products',methods=['POST','GET'])
def addProducts():
    if request.method == "POST":
        title = str(request.form['title'])
        price = str(request.form['price'])
        description = str(request.form['description'])
        if title == "" or price == "" or description == "":
            return render_template("home.html",msg="Ensure no field is empty")
        else:
            conn = makeConnection()
            cur = conn.cursor()
            sql = "INSERT INTO products(title,price,description)VALUES(%s,%s,%s)"
            cur.execute(sql,(title,price,description))
            conn.commit()
            return render_template("home.html",msg="Products Added Successfully")
    else:
        return redirect('/home')

@app.route('/register',methods=['POST','GET'])
def register():
    return render_template('register.html')

@app.route('/add-users-to-db',methods=['POST','GET'])
def addUsers():
    if request.method == "POST":
        #we proceed with the registration
        fname = str(request.form['fname'])
        lname = str(request.form['lname'])
        email = str(request.form['email'])
        password = str(request.form['password'])
        phone = str(request.form['phone'])
        message = ""
        #we check if the fields are empty
        if fname == "" or lname == "" or email == "" or password == "" or phone == "":
            return render_template("register.html",msg="Ensure none of the fields are empty")
        else:
            conn = makeConnection()
            cur = conn.cursor()
            check_sql = "SELECT email FROM users WHERE email=%s"
            check_phone = "SELECT phone FROM users WHERE phone=%s"
            cur.execute(check_sql,(email))
            cur_phone = conn.cursor()
            cur_phone.execute(check_phone, (phone))
            if cur.rowcount >= 1:
                message = "The email "+email+" is already registered"
                return render_template("register.html", msg=message)
            elif cur_phone.rowcount >= 1:
                message = "The Mobile Number " + phone + " is already registered"
                return render_template("register.html", msg=message)
            elif cur.rowcount == 0:
                sql = "INSERT INTO users(fname,lname,email,password,phone)values(%s,%s,%s,%s,%s)"
                cur.execute(sql,(fname,lname,email,password,phone))
                conn.commit()
                message = "User Has Been Added Successfully"
                return render_template("info.html",msg=message)
    else:
        #we redirect the user to the login page
        return redirect('/register')

@app.route('/login',methods=['POST','GET'])
def login():
    return render_template('login.html')

@app.route('/login-user',methods=['POST','GET'])
def loginUser():
    if request.method == "POST":
        #we check if the form has beed posted with empty fields
        email = str(request.form['email'])
        password = str(request.form['password'])
        if email == "" or password == "":
            return render_template("login.html",msg="Ensure that no field is empty")
        else:
            conn = makeConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM users WHERE email=%s AND password=%s"
            cur.execute(sql,(email,password))
            if cur.rowcount >= 1:#if this evaluates to true..
                #...then we login the user by creating a sesssion.
                session['username'] = email
                return redirect('/home')
            else:
                return render_template("login.html",msg="The Email/Password Combination is Incorrect!")

    else:
        return render_template("login.html",msg = "Wrong Request Method")

@app.route('/logout',methods=['POST','GET'])
def logout():
    session.pop('username',None)
    return redirect('/')

def makeConnection():
    host = "127.0.0.1"
    user = "root"
    password = ""
    database = "login_example" #this is the name of your database
    return pymysql.connect(host,user,password,database)

#return pymysql.connect("127.0.0.1","root","","login_example")

if __name__ == "__main__":
    app.run(debug=True)