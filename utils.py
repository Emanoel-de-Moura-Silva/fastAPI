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

def buscar_usuarios(id_usuario=None, nome=None, email=None, telefone=None, data_nascimento=None):
    condicoes = []
    params = []

    if id_usuario:
        condicoes.append("id_usuario = ?")
        params.append(id_usuario)
    if nome:
        condicoes.append("LOWER(nome) LIKE LOWER(?)")
        params.append(f"%{nome}%")
    if email:
        condicoes.append("LOWER(email) = LOWER(?)")
        params.append(email)
    if telefone:
        condicoes.append("telefone = ?")
        params.append(telefone)
    if data_nascimento:
        condicoes.append("data_nascimento = ?")
        params.append(data_nascimento)

    condicao_sql = " AND ".join(condicoes) if condicoes else "1=1"

    query = f"SELECT * FROM Usuarios WHERE {condicao_sql}"
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(query, params)
    resultado = cursor.fetchall()
    conn.close()
    return resultado


def buscar_produtos(nome=None, preco=None, categoria=None, estoque=None):
    condicoes = []
    params = []

    if nome:
        condicoes.append("LOWER(nome) LIKE LOWER(?)")
        params.append(f"%{nome}%")  # Permite buscas parciais
    if preco not in [None, 0]:  # Ignora preço se for None ou 0
        condicoes.append("preco = ?")
        params.append(preco)
    if categoria:
        condicoes.append("LOWER(categoria) LIKE LOWER(?)")
        params.append(f"%{categoria}%")  # Permite buscas parciais
    if estoque not in [None, 0]:  # Ignora estoque se for None ou 0
        condicoes.append("estoque = ?")
        params.append(estoque)

    condicao_sql = " AND ".join(condicoes) if condicoes else "1=1"
    
    query = f"SELECT * FROM Produtos WHERE {condicao_sql}"
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(query, params)
    resultado = cursor.fetchall()
    conn.close()
    return resultado


def buscar_pedidos(id_usuario=None, status=None):
    condicoes = []
    params = []

    if id_usuario is not None:  # Garante que 0 seja considerado
        condicoes.append("id_usuario = ?")
        params.append(id_usuario)
    if status:
        condicoes.append("LOWER(status) LIKE LOWER(?)")
        params.append(f"%{status}%")  # Permite buscas parciais

    condicao_sql = " AND ".join(condicoes) if condicoes else "1=1"

    query = f"SELECT * FROM Pedidos WHERE {condicao_sql}"
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(query, params)
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def buscar_enderecos(id_usuario=None, rua=None, cidade=None, estado=None, cep=None):
    condicoes = []
    params = []

    if id_usuario not in [None, 0]:  # Ignora 0 como se fosse vazio
        condicoes.append("id_usuario = ?")
        params.append(id_usuario)
    if rua:
        condicoes.append("LOWER(rua) LIKE LOWER(?)")
        params.append(f"%{rua}%")  
    if cidade:
        condicoes.append("LOWER(cidade) LIKE LOWER(?)")
        params.append(f"%{cidade}%")
    if estado:
        condicoes.append("LOWER(estado) LIKE LOWER(?)")
        params.append(f"%{estado}%")
    if cep:
        condicoes.append("cep = ?")
        params.append(cep)

    condicao_sql = " AND ".join(condicoes) if condicoes else "1=1"

    query = f"SELECT * FROM Enderecos WHERE {condicao_sql}"
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(query, params)
    resultado = cursor.fetchall()
    conn.close()
    return resultado
