import sqlite3

def criar_tabelas():
    conn = sqlite3.connect('sessoes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            semana INTEGER,
            meta INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            tipo TEXT,
            tempo_liquido TEXT,
            tempo_bruto TEXT,
            data_hora TEXT
        )
    ''')
    conn.commit()
    conn.close()

def salvar_meta(semana, meta):
    conn = sqlite3.connect('sessoes.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM metas WHERE semana = ?', (semana,))
    cursor.execute('INSERT INTO metas (semana, meta) VALUES (?, ?)', (semana, meta))
    conn.commit()
    conn.close()

def salvar_sessao(descricao, tipo, tempo_liquido, tempo_bruto):
    conn = sqlite3.connect('sessoes.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sessoes (descricao, tipo, tempo_liquido, tempo_bruto, data_hora)
        VALUES (?, ?, ?, ?, datetime('now'))
    ''', (descricao, tipo, tempo_liquido, tempo_bruto))
    conn.commit()
    conn.close()

def verificar_meta_existente(semana):
    conn = sqlite3.connect('sessoes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM metas WHERE semana = ?', (semana,))
    existe = cursor.fetchone()
    conn.close()
    return existe is not None

def buscar_sessoes_semana(semana):
    conn = sqlite3.connect('sessoes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sessoes')
    sessoes = cursor.fetchall()
    conn.close()
    return sessoes
