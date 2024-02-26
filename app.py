
from calendar import monthcalendar
from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key='hola'
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
    
    import datetime
    citas = [
    {'fecha': (2024, 2, 26), 'horario': '9:00 - 12:00'},
    # Agrega aquí más citas si es necesario
    ]
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    cal = monthcalendar(year, month)
    weeks = []
    for week in cal:
        days = []
        for day in week:
            if day == 0:
                days.append({'numero': '', 'horario': ''})
            else:
                citas_dia = [cita for cita in citas if cita['fecha'] == (year, month, day)]
                if citas_dia:
                    days.append({'numero': day, 'horario': citas_dia[0]['horario']})
                else:
                    days.append({'numero': day, 'horario': ''})
        weeks.append(days)

    return render_template('inicio.html', usuario=usuario, nombres=nombres, apellidos=apellidos, telefono=telefono, weeks=weeks, month=month)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

