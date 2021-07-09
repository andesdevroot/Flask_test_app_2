from flask import Flask, jsonify, request

app = Flask(__name__)

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

#Formulario Datos


if __name__ == '__main__':
    app.run(debug=True)


