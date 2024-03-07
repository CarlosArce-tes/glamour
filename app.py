
from calendar import monthcalendar
from flask import Flask, render_template, make_response, request, session, redirect, sessions, url_for
from flask_mysqldb import MySQL
from flask_session import Session
app = Flask(__name__)
app.secret_key='hola'
# Configurar la sesión para almacenarla en el sistema de archivos

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'carlos18'
app.config['MYSQL_DB'] = 'glamour'

mysql = MySQL(app)

@app.route('/')
def raiz():
    return render_template('index.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE usuario = %s AND password = %s', (usuario, password))
        user = cur.fetchone()
        cur.close()
        if user:
            session['usuario'] = user[3]
            session['nombres'] = user[1]
            session['apellidos'] = user[2]
            session['telefono'] = user[5]
            return redirect(url_for('inicio'))
        else:
            return 'Invalid username/password'
    return render_template('login.html')

@app.route('/inicio')
def inicio():
    if 'usuario' in session:
        usuario = session['usuario']
        nombres = session['nombres']
        apellidos = session['apellidos']
        telefono = session['telefono']
    else:
        return redirect(url_for('login'))

    return render_template('inicio.html', usuario=usuario, nombres=nombres, apellidos=apellidos, telefono=telefono)
@app.route('/perfil')
def perfil():
    if 'usuario' in session:
        usuario = session['usuario']
        nombres = session['nombres']
        apellidos = session['apellidos']
        telefono = session['telefono']
    else:
        return redirect(url_for('login'))

    return render_template('perfil.html', usuario=usuario, nombres=nombres, apellidos=apellidos, telefono=telefono)
    
@app.route('/logout')
def logout():
    session.clear()  # Eliminar la sesión del servidor

    # Eliminar la cookie de sesión del cliente
    response = make_response(redirect(url_for('raiz')))
    response.delete_cookie(app.session_cookie_name)  # Utiliza response.delete_cookie()

    # Deshabilitar la caché del navegador
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

