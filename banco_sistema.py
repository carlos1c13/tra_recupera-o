import tkinter as tk
from tkinter import ttk
import psycopg2

parametros = {
    "host": "localhost",
    "dbname": "banco_sistema",
    "user": "postgres",
    "password": "123"
}

CRIA_TABELAS = """

create table if not exists cadastro_clientes (
    cpf numeric primary key,
    nome varchar(40) not null,
    data_de_nascimento date not null,
    idade int not null
);
create table if not exists cadastro_produtos (
    id_produto varchar(40) not null,
    nome_produto varchar(40) not null, 
    data_validade date not null,
    quantidade int not null,
    preço numeric not null,
    primary key(id_produto, preço)
);
create table if not exists cadastro_vendas(
    nome_produto not null,
    semestre integer not null,
    id_produto varchar(40) not null references cadastro_produtos(id_produto),
    FOREIGN KEY (id_produto, preço) REFERENCES cadastro_produtos (id_produto, preço)
);
"""

def conecta_bd():
    conexao = None
    try:
        conexao = psycopg2.connect(**parametros)
        print("Conexão com o banco de dados realizada com sucesso!")
    except Exception as erro:
        print('[ERRO]:', erro)
    return conexao

def cria_tabelas(conexao):
    try:
        with conexao.cursor() as cursor:
            cursor.execute(CRIA_TABELAS)
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")


def lista_clientes(conexao):
    cursor = conexao.cursor()
    cursor.execute('insert into cadastro_clientes (cpf, nome, data_de_nascimento) values ( %s, %s, %s)')
    return cursor.fetchall()

def lista_produtos(conexao):
    cursor = conexao.cursor()
    cursor.execute('insert into cadastro_produtos (id_produto, nome_produto, preco_produto) values ( %s, %s, %s)')
    return cursor.fetchall()

def lista_vendas(conexao):
    cursor = conexao.cursor()
    cursor.execute('select * from cadastro_vendas join cadastro_produtos on(id_produto, preço)')
    return cursor.fetchall()

def insere_produtos(conexao, id_produtos, nome_produto, data_validade, quantidade,preço):
    try:
        cursor = conexao.cursor()
        cursor.execute('insert into cadastro_produtos (id_produto, nome_produto, quantidade,data_validade,preço) values (?, ?, ?,?,?)', (id_produtos, nome_produto, data_validade, quantidade,preço))
        conexao.commit()
        linhas = cursor.rowcount
        erro = 0
    except Exception as e:
        erro = 1
        print('Erro ao inserir produtos')
    return linhas, erro

def insere_clientes(conexao, cpf, nome, data_de_nascimento, idade):
    try:
        cursor = conexao.cursor()
        cursor.execute('insert into cadastra_clientes ( cpf, nome, data_de_nascimento) values ( ?, ?,?)', (cpf, nome, data_de_nascimento))
        conexao.commit()
        linhas = cursor.rowcount
        erro = 0
    except Exception as e:
        erro = 1
        print('Erro ao inserir clientes')
    return linhas, erro

def consulta_produtos(conexao, id_produto, preço):
    cursor = conexao.cursor()
    cursor.execute('select * from cadastro_produtos where (id_produto = ? and preço = ?);',(id_produto, preço))
    return cursor.fetchall()


def delete_produtos(conexao, id_produto,preço):
    cursor = conexao.cursor()
    cursor.execute('delete from cadastra_produtos where (id_produto = ? and preço = ?);',(id_produto,preço))
    print(f" excluida com sucesso!")
    conexao.commit()

