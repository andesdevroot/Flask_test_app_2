from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g
import sqlite3

from flask.json import htmlsafe_dumps



app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'secret'  #cokies

#helpers functions  a connection database sqlite3
def connect_db():
    sql = sqlite3.connect('C:\Sqlite\data.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_deb():
    if not hasattr(g, 'sqlite_db'):       
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):       
        g.sqlite_db.close()       

#rutas app

@app.route('/')
def index():
    session.pop('name', None)
    return 'Hello, World!'

#rutas con variables
@app.route('/home', methods=['GET', ' POST'], defaults={'name': 'Default'})
@app.route('/home/<string:name>', methods=['GET','POST'])
def home(name):
    session['name'] = name
    return render_template('home.html', name=name, display=True, mylist=[1,2,3,4,5], listofdictionaries=[{'name':'cesar'},{'name':'luis'}])
   


@app.route('/json')
def json():
    if 'name' in session:
      name = session.get('name', None)
    else:
       name = 'NotinSession!'
    return jsonify({"key": "value", 'key2': [1,2,3,4], 'name' : name})

#query string
@app.route('/query')
def query():
    name = request.args.get('name', 'Default')
    location = request.args.get('location', 'Default')       
    return '<h1>Hola {}, tu eres de {} .tu estas en la pagina QUERY!!</h1>'.format(name, location)

#Formulario con metodo POST
@app.route('/form', methods=['GET', 'POST'])
def form():
    
    if request.method == 'GET':
        return render_template('form.html')
    else:
        # name = request.form.get('name')
        # location = request.form.get('location')
        
        db = get_deb()
        db.execute('INSERT INTO users (name, locations) VALUES (?, ?)', [request.form['name'], request.form['location']])
        db.commit()
        
        # return 'Hola {}. Tu eres de {}. Tu has sido registrado exitosamente'.format(name, location)
        return redirect(url_for('home', name=request.form.get('name'), locationspy=request.form.get('locations')))


@app.route('/process', methods=['POST'])
def process():
    name = request.form.get('name')
    location = request.form.get('location')
    
    return 'Hola {}. Tu eres de {}. Tu has sido registrado exitosamente'.format(name, location)

@app.route('/processjson', methods=['POST'])
def processjson():
    
    data= request.get_json()
    
    name = data['name']
    location = data['location']
    
           
    return jsonify({'result': 'Success!', 'name': name, 'location': location})

@app.route('/viewresults')
def viewresults():       
    db = get_deb()
    cur = db.execute('select id, name, locations from users')
    results = cur.fetchall()
    return '<h1>El ID  es {}. El nombre es {}. El lugar es {}.</h1>.'.format(results[1]['id'], results[1]['name'], results[1]['locations']) 
    



if __name__ == '__main__':
    app.run()


