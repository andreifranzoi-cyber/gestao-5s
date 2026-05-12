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

    cursor.execute("SELECT * FROM auditorias ORDER BY id DESC")
    auditorias = cursor.fetchall()

    # Média geral
    cursor.execute("SELECT AVG(nota) FROM auditorias")
    media = cursor.fetchone()[0]

    if media is None:
        media = 0

    # Total auditorias
    total = len(auditorias)

    # Melhor nota
    cursor.execute("SELECT MAX(nota) FROM auditorias")
    melhor_nota = cursor.fetchone()[0]

    if melhor_nota is None:
        melhor_nota = 0

    # Medalha
    ouro = len([a for a in auditorias if a[2] >= 90])
    prata = len([a for a in auditorias if a[2] >= 80])
    bronze = len([a for a in auditorias if a[2] >= 70])

    medalha = "Nenhuma"

    if ouro >= 3:
        medalha = "🥇 Ouro"
    elif prata >= 3:
        medalha = "🥈 Prata"
    elif bronze >= 3:
        medalha = "🥉 Bronze"

    areas = [
        "Acabamento C4",
        "Inspeção Final C4",
        "Tratamento Térmico C4",
        "Tratamento Térmico Blocos",
        "Pré-acabamento C4"
    ]

    areas_auditadas = [a[1] for a in auditorias]

    faltando = len([a for a in areas if a not in areas_auditadas])

    conn.close()

    return render_template(
        'index.html',
        auditorias=auditorias,
        media=round(media, 1),
        total=total,
        melhor_nota=melhor_nota,
        medalha=medalha,
        faltando=faltando
    )

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