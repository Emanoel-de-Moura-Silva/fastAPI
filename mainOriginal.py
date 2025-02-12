from utils import *

# Exemplo de uso
if __name__ == '__main__':
    print('começando')
    criar_tabelas()

    # Exemplo de Inserção
    inserir_dados('Produtos', ['nome', 'preco', 'categoria'], ('Camiseta', 39.90, 'Roupas'))

    # Exemplo de Atualização
    atualizar_dados('Produtos', {'preco': 45.00}, "nome = 'Camiseta'")

    # Exemplo de Remoção
    remover_dados('Produtos', "nome = 'Camiseta'")

    # Exemplo de Pesquisa
    produtos = pesquisar_dados('Produtos', "categoria = 'Roupas'")
    print(produtos)

    # Exemplo de Busca com Substring
    produtos_roupas = buscar_com_substring('Produtos', 'categoria', 'roupas')
    print(produtos_roupas)

    # Exemplo de Consulta Avançada 1: Agrupamento
    #resultado_agrupamento = consulta_avancada_1()
    #print(resultado_agrupamento)

    # Exemplo de Consulta Avançada 2: JOIN
    #resultado_join = consulta_avancada_2()
    #print(resultado_join)

    # Exemplo de Consulta com ANY
    #resultado_any = consulta_any()
    #print(resultado_any)

    # Exemplo de Consulta Ordenada
    #resultado_ordenado = consulta_ordenada('Produtos', 'preco', 'DESC')
    #print(resultado_ordenado)

    # Criar gatilho
    #criar_gatilho()