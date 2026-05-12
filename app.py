from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Criar banco
def init_db():
    conn = sqlite3.connect('auditorias.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS auditorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            area TEXT,
            nota REAL,
            observacao TEXT,
            data TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# Dashboard
@app.route('/')
def index():
    conn = sqlite3.connect('auditorias.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM auditorias ORDER BY data DESC")
    auditorias = cursor.fetchall()

    conn.close()

    return render_template('index.html', auditorias=auditorias)

# Nova auditoria
@app.route('/nova', methods=['GET', 'POST'])
def nova():
    if request.method == 'POST':
        area = request.form['area']
        nota = request.form['nota']
        observacao = request.form['observacao']
        data = datetime.now().strftime('%d/%m/%Y')

        conn = sqlite3.connect('auditorias.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO auditorias (area, nota, observacao, data)
            VALUES (?, ?, ?, ?)
        ''', (area, nota, observacao, data))

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('nova_auditoria.html')

if __name__ == '__main__':
    app.run(debug=True)