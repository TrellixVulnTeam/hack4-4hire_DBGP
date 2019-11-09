from flask import Flask, render_template #Need render_template() to render HTML pages
from flask import Flask, request, flash, url_for, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:India_11@localhost/sharanud'

app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class employees(db.Model):
  
  id = db.Column('id', db.Integer, primary_key = True)
  name = db.Column(db.String(100))
  location = db.Column(db.String(50))
  mobile = db.Column(db.String(100))
  Email = db.Column(db.String(100))
  Password = db.Column(db.String(100))
  def __init__(self,name,division,Emp_id,Email,Password):
    self.name = name
    self.location = division
    self.mobile = Emp_id
    self.Email = Email
    self.Password = Password
  
@app.route('/')
def home():
  return render_template('home.html')
  
  """Render an HTML template and return"""
  # HTML file to be placed under sub-directory templates

@app.route('/about')
def about():
  return render_template('about.html')
  """Render an HTML template and return"""
   # HTML file to be placed under sub-directory templates


@app.route('/about')
def about():
  return render_template('about.html')
  """Render an HTML template and return"""
   # HTML file to be placed under sub-directory templates

@app.route('/login', methods = ['GET', 'POST'] )
def login():
  if request.method == 'POST':
    if not request.form['username'] or not request.form['password']:
      
      flash('Please Enter details', 'error')
    else:
      POST_USERNAME = str(request.form['username'])
      POST_PASSWORD = str(request.form['password'])
      
      query = employees.query.filter(employees.name==POST_USERNAME,employees.Password==POST_PASSWORD)
      result = query.first()
      if result:
        session['logged_in'] = True
        return render_template('loginSucess.html')
      else:
        flash('wrong password!')
        
  return render_template('login.html')

@app.route('/forgetpasswd', methods = ['GET', 'POST'] )
def forgetpasswd():
  return render_template('forget.html')

@app.route('/forget', methods = ['GET', 'POST'] )
def forget():
  if request.method == 'POST':
    if not request.form['Emp_id']:
      flash('Please Enter details', 'error')
    else:
      POST_EMPID = str(request.form['Emp_id'])
      return (POST_EMPID)     
      #query = employees.query.filter(employees.name==POST_USERNAME,employees.Password==POST_PASSWORD)



@app.route('/signup', methods = ['GET', 'POST'] )
def signup():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['division'] or not request.form['Emp_id'] :
        flash('Please enter all the fields', 'error')
      else:
         employee = employees(request.form['name'], request.form['division'],
            request.form['Emp_id'], request.form['Email'],request.form['Password'])
         
         db.session.add(employee)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('login'))
   return render_template('signup.html')
 
if __name__ == '__main__':
  db.create_all()
  app.run(debug=True) # Enable reloader and debugger