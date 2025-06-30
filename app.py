from flask import Flask, render_template, request, redirect, url_for
from database import criar_tabelas, salvar_meta, salvar_sessao, verificar_meta_existente
from datetime import datetime, date, timedelta
import sqlite3

app = Flask(__name__)

criar_tabelas()

def semana_periodo(ano, semana):
    primeiro_dia = date.fromisocalendar(ano, semana, 1)
    ultimo_dia = primeiro_dia + timedelta(days=6)
    return f"S{semana} - {primeiro_dia.strftime('%d/%m')} a {ultimo_dia.strftime('%d/%m')}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        descricao = request.form.get('descricao', '').strip()
        tipo = request.form.get('tipo', '').strip()
        tempo_liquido = request.form.get('tempo_liquido', '').strip()
        tempo_bruto = request.form.get('tempo_bruto', '').strip()

        if tipo and tempo_liquido and tempo_bruto:
            salvar_sessao(descricao, tipo, tempo_liquido, tempo_bruto)
            semana = datetime.today().isocalendar()[1]
            if not verificar_meta_existente(semana):
                return redirect(url_for('meta'))
            return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/meta', methods=['GET', 'POST'])
def meta():
    conn = sqlite3.connect('sessoes.db')
    cursor = conn.cursor()

    # Buscar semanas já existentes com ano
    cursor.execute("SELECT DISTINCT ano, semana FROM metas UNION SELECT DISTINCT strftime('%Y', data), strftime('%W', data) FROM sessoes")
    semanas_existentes = list(set((int(a), int(s)) for a, s in cursor.fetchall()))
    semanas_existentes.sort()

    if request.method == 'POST':
        semana_ano = request.form['semana_ano']
        ano, semana = map(int, semana_ano.split('-'))
        meta = int(request.form['meta']) * 60  # converte para minutos, se necessário

        # Atualiza se existir, senão insere
        cursor.execute("SELECT 1 FROM metas WHERE semana = ? AND ano = ?", (semana, ano))
        if cursor.fetchone():
            cursor.execute("UPDATE metas SET meta_semanal = ? WHERE semana = ? AND ano = ?", (meta, semana, ano))
        else:
            cursor.execute("INSERT INTO metas (semana, ano, meta_semanal) VALUES (?, ?, ?)", (semana, ano, meta))

        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('meta.html', semanas_existentes=semanas_existentes)



@app.route('/relatorio')
def relatorio():
    conn = sqlite3.connect('sessoes.db')
    cursor = conn.cursor()

    cursor.execute("SELECT tempo_liquido, data FROM sessoes")
    sessoes = cursor.fetchall()

    semanas = {}
    for tempo, data in sessoes:
        dt = datetime.strptime(data, '%Y-%m-%d')
        ano, semana, _ = dt.isocalendar()
        minutos = int(tempo)
        horas = minutos / 60
        key = f"{ano}-S{semana}"

        if key not in semanas:
            semanas[key] = {'total': 0, 'sessoes': 0}
        semanas[key]['total'] += horas
        semanas[key]['sessoes'] += 1

    cursor.execute("SELECT semana, ano, meta_semanal FROM metas")
    metas_db = cursor.fetchall()
    metas = {f"{ano}-S{semana}": meta / 60 for semana, ano, meta in metas_db}

    conn.close()

    todas = set(semanas.keys()).union(metas.keys())
    ordered = sorted(todas, key=lambda x: (int(x.split('-S')[0]), int(x.split('-S')[1])))

    labels = [semana_periodo(int(k.split('-S')[0]), int(k.split('-S')[1])) for k in ordered]
    valores = []
    cores = []
    metas_lista = []
    sessoes_lista = []

    for key in ordered:
        realizado = semanas.get(key, {}).get('total', 0)
        meta = metas.get(key, 0)
        sessoes = semanas.get(key, {}).get('sessoes', 0)

        cor = 'rgba(255, 60, 60, 0.7)' if realizado < meta else 'rgba(75, 192, 75, 0.7)'

        valores.append(round(realizado, 2))
        cores.append(cor)
        metas_lista.append(round(meta, 2))
        sessoes_lista.append(sessoes)

    return render_template(
        'relatorio.html',
        labels=labels,
        valores=valores,
        cores=cores,
        metas=metas_lista,
        sessoes=sessoes_lista
    )

if __name__ == '__main__':
    app.run(debug=True)
