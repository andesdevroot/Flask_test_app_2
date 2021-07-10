from flask import Flask, jsonify, request, url_for, redirect


app = Flask(__name__)

app.config['DEBUG'] = True

@app.route('/')
def index():
    return 'Hello, World!'

#rutas con variables
@app.route('/home', methods=['GET', ' POST'], defaults={'name': 'Default'})
@app.route('/home/<string:name>', methods=['GET','POST'])
def home(name):
    return '<h1>Hola {}, tu estas en la pagina home!!</h1>'.format(name)


@app.route('/json')
def json():
    return jsonify({"key": "value", 'key2': [1,2,3,4]})

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
        return '''<form method="POST" action="/form">
                <input type="text" name="name">
                <input type="text" name="location">
                <input type="submit">
                </form>'''
    else:
        # name = request.form.get('name')
        # location = request.form.get('location')
        
        # return 'Hola {}. Tu eres de {}. Tu has sido registrado exitosamente'.format(name, location)
        return redirect(url_for('home', name=request.form.get('name'), location=request.form.get('location')))


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




if __name__ == '__main__':
    app.run()


