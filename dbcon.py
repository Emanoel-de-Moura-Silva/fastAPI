import sqlite3

# conexão com o banco de dados
def conectar():
    return sqlite3.connect("banco_dados.db")

# criação das tabelas no banco de dados
def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    file_path = r"scripts\create_tables.sql"

    with open(file_path, "r", encoding="utf-8") as file:
        command = file.read()
    
    print('começando tabela')
    #print(command)

    try:
        cursor.executescript(command)
        conn.commit()
        print("Tabelas criadas com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao executar o script SQL: {e}")
    finally:
        conn.close()
