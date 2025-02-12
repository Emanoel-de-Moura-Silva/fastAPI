from dbcon import *

# Função para execução de consultas SQL
def executar_query(query, params=None):
    conn = conectar()
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    conn.commit()
    conn.close()

# Inserir dados
def inserir_dados(tabela, colunas, valores):
    query = f"INSERT INTO {tabela} ({', '.join(colunas)}) VALUES ({', '.join(['?' for _ in valores])})"
    executar_query(query, valores)

# Remover dados
def remover_dados(tabela, condicao):
    query = f"DELETE FROM {tabela} WHERE {condicao}"
    executar_query(query)

# Atualizar dados
def atualizar_dados(tabela, atualizacoes, condicao):
    query = f"UPDATE {tabela} SET {', '.join([f'{key} = ?' for key in atualizacoes.keys()])} WHERE {condicao}"
    executar_query(query, tuple(atualizacoes.values()))

# Pesquisar TABELA
def pesquisar_tabela(tabela):
    query = f"SELECT * FROM {tabela}"
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(query)
    resultado = cursor.fetchall()
    conn.close()
    return resultado

# Pesquisar dados
def pesquisar_dados(tabela, condicao):
    query = f"SELECT * FROM {tabela} WHERE {condicao}"
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(query)
    resultado = cursor.fetchall()
    conn.close()
    return resultado

# Manipulação em Massa
def inserir_em_massa(tabela, colunas, lista_dados):
    query = f"INSERT INTO {tabela} ({', '.join(colunas)}) VALUES ({', '.join(['?' for _ in colunas])})"
    conn = conectar()
    cursor = conn.cursor()
    cursor.executemany(query, lista_dados)
    conn.commit()
    conn.close()

# Busca com Substring (case insensitive)
def buscar_com_substring(tabela, coluna, substring):
    query = f"SELECT * FROM {tabela} WHERE LOWER({coluna}) LIKE LOWER(?)"
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(query, ('%' + substring + '%',))
    resultado = cursor.fetchall()
    conn.close()
    return resultado

# Consultas Avançadas
def consulta_avancada_1():
    query = """
    SELECT categoria, COUNT(*) as total_produtos
    FROM Produtos
    GROUP BY categoria
    HAVING COUNT(*) > 5
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(query)
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def consulta_avancada_2():
    query = """
    SELECT u.nome, COUNT(p.id_pedido) as total_pedidos
    FROM Usuarios u
    JOIN Pedidos p ON u.id_usuario = p.id_usuario
    GROUP BY u.id_usuario
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(query)
    resultado = cursor.fetchall()
    conn.close()
    return resultado

# Consulta com quantificador ANY
def consulta_any():
    query = """
    SELECT nome, preco
    FROM Produtos
    WHERE preco > ANY (SELECT preco FROM Produtos WHERE categoria = 'Eletrônicos')
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(query)
    resultado = cursor.fetchall()
    conn.close()
    return resultado

# Consulta com ordenação
def consulta_ordenada(tabela, coluna, ordem='ASC'):
    query = f"SELECT * FROM {tabela} ORDER BY {coluna} {ordem}"
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(query)
    resultado = cursor.fetchall()
    conn.close()
    return resultado

# Criar gatilho
def criar_gatilho():
    query = """
    CREATE TRIGGER IF NOT EXISTS after_insert_pedido
    AFTER INSERT ON Pedidos
    BEGIN
        UPDATE Usuarios SET status = 'Novo Pedido' WHERE id_usuario = NEW.id_usuario;
    END
    """
    executar_query(query)
